-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 03-04-2020 a las 03:02:29
-- Versión del servidor: 10.4.11-MariaDB
-- Versión de PHP: 7.4.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `pt_cycling`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `game`
--

CREATE TABLE `game` (
  `game_id` int(11) NOT NULL,
  `game_data_create` datetime NOT NULL DEFAULT current_timestamp(),
  `game_num_players` int(11) NOT NULL,
  `game_player_id_master` int(11) NOT NULL,
  `game_players_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`game_players_id`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Volcado de datos para la tabla `game`
--

INSERT INTO `game` (`game_id`, `game_data_create`, `game_num_players`, `game_player_id_master`, `game_players_id`) VALUES
(1, '2020-04-02 22:00:41', 2, 1, '[1]');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `player`
--

CREATE TABLE `player` (
  `player_id` int(11) NOT NULL,
  `player_name` text COLLATE utf8_bin NOT NULL,
  `player_date_create` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Volcado de datos para la tabla `player`
--

INSERT INTO `player` (`player_id`, `player_name`, `player_date_create`) VALUES
(1, 'lautiMan', '2020-04-02 22:00:10');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `player_data`
--

CREATE TABLE `player_data` (
  `player_data_id` int(11) NOT NULL,
  `player_data_player_id` int(11) NOT NULL,
  `player_data_date_server` datetime NOT NULL DEFAULT current_timestamp(),
  `player_data_date_player` datetime NOT NULL,
  `player_data_distance` float NOT NULL,
  `player_data_speed_max` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Volcado de datos para la tabla `player_data`
--

INSERT INTO `player_data` (`player_data_id`, `player_data_player_id`, `player_data_date_server`, `player_data_date_player`, `player_data_distance`, `player_data_speed_max`) VALUES
(1, 1, '2020-04-02 21:58:16', '2020-04-02 21:57:45', 1, 10),
(2, 1, '2020-04-02 21:58:40', '2020-04-02 21:57:45', 1, 10);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `game`
--
ALTER TABLE `game`
  ADD PRIMARY KEY (`game_id`);

--
-- Indices de la tabla `player`
--
ALTER TABLE `player`
  ADD PRIMARY KEY (`player_id`);

--
-- Indices de la tabla `player_data`
--
ALTER TABLE `player_data`
  ADD PRIMARY KEY (`player_data_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `game`
--
ALTER TABLE `game`
  MODIFY `game_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `player`
--
ALTER TABLE `player`
  MODIFY `player_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `player_data`
--
ALTER TABLE `player_data`
  MODIFY `player_data_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
