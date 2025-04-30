-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 27-11-2024 a las 13:37:48
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `restaurante`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categoria`
--

CREATE TABLE `categoria` (
  `idcategoria` int(11) NOT NULL,
  `nombrecat` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `categoria`
--

INSERT INTO `categoria` (`idcategoria`, `nombrecat`) VALUES
(1, 'Bebidas'),
(2, 'Comidas'),
(3, 'Pastelería'),
(4, 'Panes'),
(5, 'Sin TACC');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `menu`
--

CREATE TABLE `menu` (
  `idmenu` int(11) NOT NULL,
  `nombremenu` varchar(200) DEFAULT NULL,
  `descrimenu` varchar(200) DEFAULT NULL,
  `preciomenu` float DEFAULT NULL,
  `urlimg` varchar(150) NOT NULL,
  `idcategoria` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `menu`
--

INSERT INTO `menu` (`idmenu`, `nombremenu`, `descrimenu`, `preciomenu`, `urlimg`, `idcategoria`) VALUES
(1, 'Café Espresso', 'Un café intenso, preparado con granos recién molidos.', 4000.9, '/static/cafeexpresso.png', 1),
(2, 'Café Capucchino', 'Un café intenso, preparado con granos recién molidos', 1800, '/static/cafecapuchino.png', 1),
(3, 'Café Late', 'Un café intenso, preparado con granos recién molidos', 2000, '/static/cafelatte.png', 1),
(4, 'Lasaña', 'Lasaña de carne', 1500, '/static/lasana.png', 2),
(5, 'Milanesa a la Napolitana con crema', 'Milanesa a la napolitana con Papas fritas', 2000, '/static/milanesa.jpg', 2),
(6, 'Hamburguesa', 'Hamburguesa doble carne con vegetales', 2000, '/static/hamburguesa.png', 2),
(7, 'Torta Tres Leches', 'Torta fría de tres leches y chocolate', 3200, '/static/torta3leches.png', 3),
(8, 'Torta Chocolate', 'Torta rellena de chocolate', 3400, '/static/chocolate.png', 3),
(9, 'Albóndigas con Puré de Papas', 'Albóndigas con Puré de Papas', 1800, '/static/albondigas.jpg', 2),
(11, 'Crema de Zanahoria con crema', 'Crema de Zanahoria con crema', 5000, '/static/creamazana.jpg', 2);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `categoria`
--
ALTER TABLE `categoria`
  ADD PRIMARY KEY (`idcategoria`);

--
-- Indices de la tabla `menu`
--
ALTER TABLE `menu`
  ADD PRIMARY KEY (`idmenu`),
  ADD KEY `idcategoria` (`idcategoria`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `menu`
--
ALTER TABLE `menu`
  MODIFY `idmenu` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `menu`
--
ALTER TABLE `menu`
  ADD CONSTRAINT `menu_ibfk_1` FOREIGN KEY (`idcategoria`) REFERENCES `categoria` (`idcategoria`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
