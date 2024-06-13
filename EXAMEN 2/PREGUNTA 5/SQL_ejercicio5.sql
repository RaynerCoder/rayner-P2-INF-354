
/*
--EJECUTAR PRIMERO LA FUNCION
CREATE FUNCTION dbo.CalcularUnosEnMatriz (
    @nombre1 VARCHAR(20),
    @nombre2 VARCHAR(20)
)
RETURNS INT
AS
BEGIN
    DECLARE @longitud INT;
    DECLARE @contador INT = 0;
    DECLARE @totalUnos INT = 0;
    DECLARE @caracter VARCHAR(20);
    DECLARE @campo VARCHAR(10);

    SELECT @longitud = LEN(@nombre2);
    SELECT @contador = 0;

    WHILE @contador < @longitud
    BEGIN
        SET @caracter = LEFT(@nombre2, 1); -- Obtener el primer caracter de la izquierda 'nombre2'
        SET @nombre2 = RIGHT(@nombre2, LEN(@nombre2) - 1); -- Obtener todos los caracteres menos el primero 'nombre2'
        SELECT TOP 1 @campo = COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = 'nombre' 
        AND LEFT(COLUMN_NAME, 1) = @caracter 
        AND ORDINAL_POSITION >= (@contador + 1);

        IF @campo IS NOT NULL
        BEGIN
            SET @totalUnos = @totalUnos + 1;
        END

        SET @contador = @contador + 1;
    END

    RETURN @totalUnos;
END;
*/



-- Paso 1: Crear la tabla alumno
DROP TABLE alumno;
CREATE TABLE alumno (
    id INT,
    nombre VARCHAR(20),
    paterno VARCHAR(20)
);

-- Paso 2: Insertar datos en la tabla alumno
INSERT INTO alumno VALUES (43, 'm', 'a');
INSERT INTO alumno VALUES (4, 'a', 'b');

-- Paso 3: Mostrar las tablas y columnas en la base de datos
SELECT table_name = 'alumno';

-- Paso 4: Borrar la tabla nombre si existe
DROP TABLE nombre;

DECLARE
    @nombre1 VARCHAR(20), 
    @nombre2 VARCHAR(20),
    @caracter VARCHAR(20),
    @contador INT, 
    @longitud INT,
    @campo VARCHAR(10),
    @sql NVARCHAR(2000), 
    @sql2 NVARCHAR(2000);

SET @nombre1 = 'martha';
SET @nombre2 = 'marta';
PRINT @nombre1;

-- Paso 5: Crear la tabla dinámica nombre
SELECT @longitud = LEN(@nombre1); 
SELECT @contador = 0;
SET @sql = 'CREATE TABLE nombre (';
SET @sql2 = '';

WHILE @contador < @longitud
BEGIN
    SET @caracter = LEFT(@nombre1,1); -- Obtener el primer caracter de la izquierda 
    SET @nombre1 = RIGHT(@nombre1, LEN(@nombre1) - 1); -- Obtener todos los caracteres menos el primero
    PRINT @caracter;
    -- Añadir una nueva columna en cada iteración del bucle
    SET @sql = @sql + @caracter + CAST(@contador + 1 AS VARCHAR(2)) + ' INT,';
    SET @sql2 = @sql2 + 'SUM(ISNULL('+ @caracter + CAST(@contador + 1 AS VARCHAR(2)) + ', 0))+'; -- Sumará todos los valores de la columna x, tratando los NULL como 0.
    SET @contador = @contador + 1;
END

SET @sql = LEFT(@sql, LEN(@sql) - 1); -- Obtener todos los caracteres menos el último
SET @sql = @sql + ')';
PRINT @sql; -- Resultado SQL 1: create table nombre (m1 int,a2 int,r3 int,t4 int,h5 int,a6 int)

EXEC sp_executesql @sql;



-- Paso 6: Llenar la tabla nombre
SELECT @longitud = LEN(@nombre2);
SELECT @contador = 0;

WHILE @contador < @longitud
BEGIN
    SET @caracter = LEFT(@nombre2, 1); -- Obtener el primer caracter de la izquierda 'nombre2'
    SET @nombre2 = RIGHT(@nombre2, LEN(@nombre2) - 1); -- Obtener todos los caracteres menos el primero 'nombre2'
    SELECT TOP 1 @campo = COLUMN_NAME
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_NAME = 'nombre' 
    AND LEFT(COLUMN_NAME, 1) = @caracter 
    AND ORDINAL_POSITION >= (@contador + 1);
    
    -- Insertar un valor en una columna específica de la tabla nombre
    SET @sql = 'INSERT INTO nombre(' + @campo + ') VALUES (1)'; 
    EXEC sp_executesql @sql; -- Resultado primera iteración: insert into nombre(m1) values (1)
    SET @contador = @contador + 1;
END

SET @sql2 = LEFT(@sql2, LEN(@sql2) - 1); -- Obtener todos los caracteres menos el último
SET @sql2 = 'SELECT ' + @sql2 + ' FROM nombre';
PRINT @sql2; -- Resultado SQL 2: sum(ISNULL(m1, 0))+sum(ISNULL(a2, 0))+sum(ISNULL(r3, 0))+sum(ISNULL(t4, 0))+sum(ISNULL(h5, 0))+sum(ISNULL(a6, 0))

SELECT * FROM nombre;

DECLARE @nombre11 VARCHAR(20) = 'martha';
DECLARE @nombre22 VARCHAR(20) = 'marta';

-- Obtener la cantidad de unos en la matriz
SELECT dbo.CalcularUnosEnMatriz(@nombre11, @nombre22) AS TotalUnos;







