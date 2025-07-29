-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 29-07-2025 a las 15:40:11
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
-- Estructura de tabla para la tabla `empresa`
--

CREATE TABLE `empresa` (
  `idempresa` int(11) NOT NULL,
  `rifemp` varchar(50) DEFAULT NULL,
  `nombremp` varchar(200) DEFAULT NULL,
  `descripemp` varchar(200) DEFAULT NULL,
  `direccemp` varchar(200) DEFAULT NULL,
  `horario` varchar(200) DEFAULT NULL,
  `logoemp` varchar(200) DEFAULT NULL,
  `portadaemp` varchar(200) DEFAULT NULL,
  `mapa` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `empresa`
--

INSERT INTO `empresa` (`idempresa`, `rifemp`, `nombremp`, `descripemp`, `direccemp`, `horario`, `logoemp`, `portadaemp`, `mapa`) VALUES
(1, 'J23456790', 'LA CASITA DE LOLA', 'RESTAURANTE COMIDA CASERA', 'CALLE 13 CON 5TA AVENIDA SAN FELIPE YARACUY', '08:00 AM A 12:00 PM', 'logoemp.png', 'portadaemp.png', 'https://maps.app.goo.gl/csN68zY7EKb31Qcx6');

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
(1, 'Café Espresso', 'Un café intenso, preparado con granos recién molidos.', 7000, 'cafeexpresso.png', 1),
(2, 'Café Capucchino', 'Un café intenso, preparado con granos recién molidos', 1800, 'cafecapuchino.png', 1),
(3, 'Café Late', 'Un café intenso, preparado con granos recién molidos', 2000, 'cafelatte.png', 1),
(4, 'Lasaña', 'Lasaña de carne', 1500, 'lasana.png', 2),
(5, 'Milanesa a la Napolitana con crema', 'Milanesa a la napolitana con Papas fritas', 2000, 'milanesa.jpg', 2),
(6, 'Hamburguesa', 'Hamburguesa doble carne con vegetales', 2000, 'hamburguesa.jpeg', 2),
(7, 'Torta Tres Leches', 'Torta fría de tres leches y chocolate', 3200, 'torta3leches.png', 3),
(9, 'Albóndigas con Puré de Papas', 'Albóndigas con Puré de Papas', 1800, 'albondigas.jpg', 2),
(11, 'Crema de Zanahoria con crema', 'Crema de Zanahoria con crema', 5000, 'creamazana.jpg', 2),
(12, 'Pan Pinitas', 'Pan dulce azucarado', 1500, 'pan1.jpeg', 4);

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
  MODIFY `idmenu` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

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
