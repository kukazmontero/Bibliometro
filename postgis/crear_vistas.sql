-- Esperar que la BD esté lista
DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM pg_database WHERE datname = 'metro_santiago_3') THEN
    CREATE VIEW v_estaciones AS 
    SELECT * 
    FROM estaciones
      JOIN coordenadas USING (estacion);

    CREATE VIEW v_conexiones AS
    SELECT 
      c.*,
      origen.geom AS origen_geom,
      destino.geom AS destino_geom
    FROM conexiones AS c
    JOIN coordenadas AS origen 
      ON origen.estacion = c.estacion_origen
    JOIN coordenadas AS destino  
      ON destino.estacion = c.estacion_destino;
  END IF;
END $$;