
nombre y atributos de la tabla


CREATE TABLE IF NOT EXISTS automovil(
id SERIAL PRIMARY KEY NOT NULL,
marca VARCHAR(255) NOT NULL,
modelo VARCHAR(255) NOT NULL,
fecha VARCHAR(255) NOT NULL,
duenos VARCHAR(255) NOT NULL,
costos VARCHAR(255) NOT NULL,
choques VARCHAR(255) NOT NULL
);

select * from automovil