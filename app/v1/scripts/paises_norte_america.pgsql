-- Primero, obtenemos el ID del continente "Norteamérica"
SELECT p.nombre AS pais, i.nombre AS idioma
FROM pais p
JOIN pais_idioma pi ON p.id = pi.id_pais
JOIN idioma i ON pi.id_idioma = i.id
JOIN pais_continente pc ON p.id = pc.id_pais
JOIN continente c ON pc.id_continente = c.id
WHERE c.nombre = 'North America'
ORDER BY p.nombre;