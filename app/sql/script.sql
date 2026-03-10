-- Crear base de datos
CREATE DATABASE prueba;


-- Crear tabla
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARC-HAR(20) NOT NULL,
    apellido VARCHAR(20) NOT NULL,
    cedula VARCHAR(20) NOT NULL,
    edad INTEGER NOT NULL,
    usuario VARCHAR(20) NOT NULL,
    contrasena VARCHAR(20) NOT NULL
);

-- Insertar registro
INSERT INTO usuarios (nombre, apellido, cedula, edad, usuario, contrasena)
VALUES ('pedro', 'perez', '10102020', 30, 'pperez', '12345');


-- Crear tabla perfil
-- Crear tabla
CREATE TABLE perfil (
    id SERIAL PRIMARY KEY,
    nombre varchar(50) not null,
    desrcripcion varchar(100) not null
);

insert into perfil (nombre, desrcripcion)
values ('administrador', 'perfil administrador ');

-- Crear tabla clientes
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL,
    apellido VARCHAR(20) NOT NULL,
    cedula VARCHAR(20) NOT NULL,
    edad INTEGER NOT NULL,
    usuario VARCHAR(20) NOT NULL,
    contrasena VARCHAR(20) NOT NULL
);

-- Insertar registro de ejemplo
INSERT INTO clientes (nombre, apellido, cedula, edad, usuario, contrasena)
VALUES ('juan', 'garcia', '20304050', 35, 'jgarcia', '54321');