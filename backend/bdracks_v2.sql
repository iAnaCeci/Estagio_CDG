-- MySQL Script generated by MySQL Workbench
-- Wed May 8 14:09:14 2024
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema bdracks
-- -----------------------------------------------------

CREATE SCHEMA IF NOT EXISTS `bdracks` DEFAULT CHARACTER SET utf8 ;
USE `bdracks` ;

-- -----------------------------------------------------
-- Table `bdracks`.`Rack`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bdracks`.`Rack` (
  `idRack` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(45) NULL,
  `localizacao` VARCHAR(45) NULL,
  `descricao` VARCHAR(45) NULL,
  PRIMARY KEY (`idRack`)
) ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bdracks`.`Gaveta`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bdracks`.`Gaveta` (
  `idGaveta` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(45) NULL,
  `descricao` VARCHAR(45) NULL,
  `estado` VARCHAR(45) NULL,
  `Rack_idRack` INT NOT NULL,
  PRIMARY KEY (`idGaveta`),
  CONSTRAINT `fk_Gavetas_Rack`
    FOREIGN KEY (`Rack_idRack`)
    REFERENCES `bdracks`.`Rack` (`idRack`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION
) ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bdracks`.`Registro`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bdracks`.`Registro` (
  `idRegistro` INT NOT NULL AUTO_INCREMENT,
  `data` DATE NULL,
  `hora` TIME NULL,
  `cor` VARCHAR(45) NULL,
  `observacao` TEXT NULL,
  `Gaveta_idGaveta` INT NOT NULL,
  PRIMARY KEY (`idRegistro`),
  CONSTRAINT `fk_Registro_Gaveta1`
    FOREIGN KEY (`Gaveta_idGaveta`)
    REFERENCES `bdracks`.`Gaveta` (`idGaveta`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE = InnoDB;

ALTER TABLE Registro MODIFY COLUMN idRegistro INT AUTO_INCREMENT;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
