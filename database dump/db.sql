-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Czas generowania: 07 Wrz 2022, 19:52
-- Wersja serwera: 8.0.26
-- Wersja PHP: 8.0.23

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Baza danych: `s405512`
--

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `message`
--

CREATE TABLE `message` (
  `id` int NOT NULL,
  `user_id` int NOT NULL,
  `content` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Zrzut danych tabeli `message`
--

INSERT INTO `message` (`id`, `user_id`, `content`, `created_at`) VALUES
(1, 2, 'Wassup!', '2022-09-05 23:17:02'),
(2, 1, 'Howdy Mister', '2022-09-05 23:37:05'),
(3, 3, 'Hello there!', '2022-09-05 23:37:39'),
(4, 2, 'how\'s life?', '2022-09-05 23:17:02'),
(5, 1, 'good good..', '2022-09-05 23:37:05'),
(6, 2, 'damn, it\'s pretty late ', '2022-09-05 23:17:02'),
(7, 3, 'I\'m fine and how about you', '2022-09-05 23:37:39'),
(8, 1, 'yeah', '2022-09-05 23:37:05'),
(9, 1, 'this game is awesome!', '2022-09-05 23:37:05'),
(10, 2, 'It\'s gret ngl', '2022-09-05 23:17:02'),
(11, 1, 'i love this game ', '2022-09-05 23:37:05'),
(12, 2, '*great', '2022-09-05 23:17:02'),
(13, 3, 'mom calls me for dinner', '2022-09-05 23:37:39'),
(14, 3, 'I\'m back', '2022-09-06 17:09:29'),
(15, 5, 'dhads', '2022-09-06 17:01:09'),
(16, 7, 'aasd', '2022-09-07 21:37:09');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `mission`
--

CREATE TABLE `mission` (
  `id` int NOT NULL,
  `title` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `danger_level` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Zrzut danych tabeli `mission`
--

INSERT INTO `mission` (`id`, `title`, `content`, `danger_level`) VALUES
(1, 'Find a criminal', 'A weapon smuggler has been seen on planet X-512. Capture him dead or alive.', 1),
(2, 'Protect VIP', 'Senate member needs protection, during his travel.', 2),
(3, 'Destroy rebels camp', 'Imperium has been troubled by small rebels camp located near 3F3-G42 sector. Find it and destroy it.', 3),
(4, 'Alien eggs', 'It\'s hatching season for Irraik. Their eggs may not look like much, but traders pay well for them.', 1),
(5, 'Catch the chickens', 'Catch chickens for local shopkeeper.', 2),
(6, 'Fight the droids', 'A group of droids has been spotted in the area destroying buildings. Eliminate them.', 3),
(7, 'Escort a trade ship', 'Trade ship requires escort to reach the base.', 1),
(8, 'Repair the traveler\'s ship', 'Traveler stuck nearby because his ship was damaged. Help fix it', 2),
(9, 'Space pirates on my spaceship', 'Pirates took over my spaceship, I need immediate help!', 3),
(10, 'Space wolves', 'Bring me 10 space wolf skins.', 1),
(11, 'Galatic spiders', 'A pack of galactic spiders was seen in the nearest space cave. Please take care of them.', 2),
(12, 'Extraterrestial monkes', 'Those animals are throwing their bananas everywhere! Please, get rid of them!', 3);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `mission_handler`
--

CREATE TABLE `mission_handler` (
  `id` int NOT NULL,
  `user_id` int NOT NULL,
  `last_missions_update` datetime NOT NULL,
  `mission_taken_time` datetime DEFAULT NULL,
  `easy_mission_id` int DEFAULT NULL,
  `medium_mission_id` int DEFAULT NULL,
  `hard_mission_id` int DEFAULT NULL,
  `mission_picked_id` int DEFAULT NULL,
  `easy_mission_cost` int DEFAULT NULL,
  `medium_mission_cost` int DEFAULT NULL,
  `hard_mission_cost` int DEFAULT NULL,
  `easy_mission_duration` int DEFAULT NULL,
  `medium_mission_duration` int DEFAULT NULL,
  `hard_mission_duration` int DEFAULT NULL,
  `mission_bg` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Zrzut danych tabeli `mission_handler`
--

INSERT INTO `mission_handler` (`id`, `user_id`, `last_missions_update`, `mission_taken_time`, `easy_mission_id`, `medium_mission_id`, `hard_mission_id`, `mission_picked_id`, `easy_mission_cost`, `medium_mission_cost`, `hard_mission_cost`, `easy_mission_duration`, `medium_mission_duration`, `hard_mission_duration`, `mission_bg`) VALUES
(1, 1, '2022-09-06 17:21:54', NULL, 4, 2, 3, -1, 7, 15, 23, 18, 40, 108, 4),
(2, 2, '2022-09-06 17:22:29', '2022-09-06 17:22:30', 1, 8, 9, 0, 7, 13, 18, 14, 27, 43, 5),
(3, 3, '2022-09-06 17:11:28', '2022-09-06 17:11:31', 4, 11, 3, 0, 10, 14, 18, 30, 57, 85, 4),
(4, 4, '2022-09-06 17:09:29', NULL, 1, 2, 3, 0, 5, 12, 26, 30, 60, 120, 1),
(5, 5, '2022-09-06 17:19:45', '2022-09-06 17:20:40', 1, 2, 12, 0, 9, 12, 17, 22, 48, 105, 4),
(6, 6, '2022-09-06 21:12:16', '2022-09-06 21:11:22', 10, 8, 3, -1, 8, 14, 23, 14, 22, 52, 2),
(7, 7, '2022-09-07 21:49:23', '2022-09-07 21:49:25', 4, 8, 12, 0, 9, 14, 24, 14, 20, 44, 1);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `user`
--

CREATE TABLE `user` (
  `id` int NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `password` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `name` varchar(1000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `confirmed` tinyint(1) NOT NULL,
  `character_type` int DEFAULT NULL,
  `current_health` int DEFAULT NULL,
  `max_health` int DEFAULT NULL,
  `money` int DEFAULT NULL,
  `speed` int DEFAULT NULL,
  `armor` int DEFAULT NULL,
  `luck` int DEFAULT NULL,
  `is_free` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `last_death_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Zrzut danych tabeli `user`
--

INSERT INTO `user` (`id`, `email`, `password`, `name`, `confirmed`, `character_type`, `current_health`, `max_health`, `money`, `speed`, `armor`, `luck`, `is_free`, `last_death_time`) VALUES
(1, 'money@dot.pl', 'sha256$LaLDAwfGoScasjx9$c2d622621f2c02e25c2f561e6cc7be7cfaa89265a37d51c1cbdc8103d30e105c', 'Boxguy', 1, 3, 100, 100, 9970, 2, 1, 2, 'true', '0001-01-01 00:00:00'),
(2, 'dead@dot.pl', 'sha256$9QgDXyfHX6O7N2yH$5f6813659577cea8e7bbd406df176d9c9bc277b72fd137fa16a4b34058976a42', 'Muted13', 1, 2, 100, 100, 685, 7, 1, 1, 'true', '2022-09-06 17:22:47'),
(3, 'capitan@gmail.com', 'sha256$JlVX7SiF9Y8pOH2H$2d03cdcc0e5e4966808049926e001f3c5361a9ca72cc5cbb30d2cd4e5a9e3851', 'Capitan', 1, 3, 99, 100, 20, 1, 1, 1, 'true', '0001-01-01 00:00:00'),
(4, 'jacek@gmail.com', 'sha256$G9LW8qWWFIY0faIp$49fe36dc7f0052456c3091da1ebadd36ce324ae0711672a6e57bd040a2035163', 'Jacek', 1, 0, 100, 100, 10, 1, 1, 1, 'true', '0001-01-01 00:00:00'),
(5, 'test@dot.pl', 'sha256$kyBS3HAeurwEgh6e$d350de24b43bf1ea1c43a29acb324264230d4bfc929e037c3297a45d31575681', 'Test', 1, 1, 94, 100, 19, 1, 1, 1, 'true', '0001-01-01 00:00:00'),
(6, 'new@gg.pl', 'sha256$4DtU5jraswVoOBn8$7ce58aa9587eea73bf2e51a63109b07a988e5ebd2b9ff777a1181c693a83ccd2', 'New', 1, 2, 100, 100, 1325, 10, 1, 2, 'true', '2022-09-06 21:11:39'),
(7, 'admin@admin.pl', 'sha256$c8ILsaYgJdHQqwUc$aa04ad387905998d9d25bd717e1058aa6a2e0d68a96e90b172b2b19fb99ef81c', 'Admin', 1, 2, 84, 100, 778, 9, 1, 2, 'true', '2022-09-07 21:45:29');

--
-- Indeksy dla zrzutów tabel
--

--
-- Indeksy dla tabeli `message`
--
ALTER TABLE `message`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indeksy dla tabeli `mission`
--
ALTER TABLE `mission`
  ADD PRIMARY KEY (`id`);

--
-- Indeksy dla tabeli `mission_handler`
--
ALTER TABLE `mission_handler`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indeksy dla tabeli `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT dla zrzuconych tabel
--

--
-- AUTO_INCREMENT dla tabeli `message`
--
ALTER TABLE `message`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT dla tabeli `mission`
--
ALTER TABLE `mission`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT dla tabeli `mission_handler`
--
ALTER TABLE `mission_handler`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT dla tabeli `user`
--
ALTER TABLE `user`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Ograniczenia dla zrzutów tabel
--

--
-- Ograniczenia dla tabeli `message`
--
ALTER TABLE `message`
  ADD CONSTRAINT `message_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Ograniczenia dla tabeli `mission_handler`
--
ALTER TABLE `mission_handler`
  ADD CONSTRAINT `mission_handler_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
