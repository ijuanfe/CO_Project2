include "Datos1.dzn";
% Complejidad y Optimización: Proyecto 2
% Problema Plantas de Energía: Modelo genérico

% Nota: Ejecutar con COIN-BC: da soporte a variables flotantes

% 1. Parámetros: datos cargados de archivo Datos.dzn
int: Nc; % Número de centrales eléctricas
int: S;  % Número de clientes
int: n;  % Número de días para satisfacer demanda diaria de clientes
set of int: Centrales = 1..Nc;
set of int: Clientes = 1..S;
set of int: Dias = 1..n;
array [Centrales] of float: CaP; % Capacidad de producción diaria en megawatts (MW) por central eléctrica
array [Centrales] of float: CoP; % Costo producción de un MW por central eléctrica
array [Clientes, Dias] of float: d; % Demanda diaria de energía eléctrica en MW por cliente en un rango de días


% % 2. Variable de decisión
% % Energía eléctrica diaria en MW suministrada a cada cliente desde cada central en un rango de días
array [Centrales, Dias, Clientes] of var float: ES;


% % 3. Restricciones
% % 3.1 No negatividad
constraint Nc >= 0;
constraint S >= 0;
constraint n >= 0;
constraint forall ( i in Centrales )( CaP[i] >= 0.0);
constraint forall ( i in Centrales )( CoP[i] >= 0.0);
constraint forall ( i in Clientes )(
            forall ( j in Dias ) (
             d[i,j] >= 0.0
            )
           );
constraint forall( i in Centrales )(
            forall( j in Dias )(
             forall( k in Clientes )(
              ES[i, j, k] >= 0
             )
            )  
           );

% % 3.2 No superar la capacidad de producción diaria por central eléctrica
constraint forall( i in Centrales )(
            forall( j in Dias )(
             sum( k in Clientes )( % La suma del suministro de todos los clientes por central
              ES[i, j, k]          % y día debe ser menor o igual a la capacidad de cada central
             ) <= CaP[i]
            )
           );

% % 3.3 Suplir la demanda diaria de energía eléctrica de los clientes
constraint forall( i in Clientes )(
            forall( j in Dias )(
             sum( k in Centrales )( % La suma del suministro entre todas las centrales
              ES[k, j, i]           % debe ser igual a la demanda del cliente en ese día
             ) = d[i, j]
            )
           );


% % 4. Función objetivo
var float: F;
F = sum( i in Centrales )(
     sum( j in Dias )(
      sum( k in Clientes )(
       ES[i, j, k] * CoP[i]
      )
     )
    );


solve minimize F;

output ["\nFilas: \(n) Días, Columnas: \(S) Clientes\n\nCentral Eléctrica 1:\n\n"] ++
       [show_float(8, 2, ES[i, j, k]) ++
           % Salta en el último cliente del mismo día
           if k == S then "\n" else " " endif ++
           % Salta cuando termina todos los días y todos los clientes de esos días, ósea salta a la siguiente central
           if (j == n /\ k == S) then if i<Nc then "\nCentral Eléctrica \(i+1):\n\n" else "" endif else "" endif |
           i in Centrales, j in Dias, k in Clientes];

output ["\nCosto mínimo: $\(F)\n\n"];
