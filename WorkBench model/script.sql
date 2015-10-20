SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `myForumApi` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `myForumApi` ;

-- -----------------------------------------------------
-- Table `myForumApi`.`User`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `myForumApi`.`User` (
  `userId` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NULL,
  `about` VARCHAR(5000) NULL,
  `name` VARCHAR(45) NULL,
  `email` VARCHAR(45) NOT NULL,
  `isAnonymous` TINYINT(1) NULL DEFAULT 0,
  PRIMARY KEY (`userId`, `email`),
  UNIQUE INDEX `user_id_UNIQUE` (`userId` ASC),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `myForumApi`.`Forum`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `myForumApi`.`Forum` (
  `forumId` INT NOT NULL AUTO_INCREMENT,
  `userEmail` VARCHAR(45) NULL,
  `shortName` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`forumId`, `shortName`, `name`),
  UNIQUE INDEX `idForum_UNIQUE` (`forumId` ASC),
  UNIQUE INDEX `Forumcol_UNIQUE` (`shortName` ASC),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC),
  INDEX `fk_ForumUserEmail_idx` (`userEmail` ASC),
  CONSTRAINT `fk_ForumUserEmail`
    FOREIGN KEY (`userEmail`)
    REFERENCES `myForumApi`.`User` (`email`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `myForumApi`.`Thread`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `myForumApi`.`Thread` (
  `threadId` INT NOT NULL AUTO_INCREMENT,
  `forumShortName` VARCHAR(45) NULL,
  `userEmail` VARCHAR(45) NULL,
  `title` VARCHAR(45) NULL,
  `slug` VARCHAR(45) NULL,
  `message` VARCHAR(4000) NULL,
  `date` DATETIME NULL,
  `isClosed` TINYINT(1) NULL DEFAULT 0,
  `isDeleted` TINYINT(1) NULL DEFAULT 0,
  `likes` INT NULL DEFAULT 0,
  `dislikes` INT NULL DEFAULT 0,
  `points` INT NULL DEFAULT 0,
  PRIMARY KEY (`threadId`),
  UNIQUE INDEX `threadId_UNIQUE` (`threadId` ASC),
  INDEX `fk_userId_idx` (`userEmail` ASC),
  INDEX `fk_forumId_idx` (`forumShortName` ASC),
  CONSTRAINT `fk_ThreadUserEmail`
    FOREIGN KEY (`userEmail`)
    REFERENCES `myForumApi`.`User` (`email`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `fk_ThreadForumShortName`
    FOREIGN KEY (`forumShortName`)
    REFERENCES `myForumApi`.`Forum` (`shortName`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `myForumApi`.`Post`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `myForumApi`.`Post` (
  `postId` INT NOT NULL AUTO_INCREMENT,
  `threadId` INT NULL,
  `userEmail` VARCHAR(45) NULL,
  `parent` INT NULL DEFAULT NULL,
  `datePost` DATETIME NULL,
  `message` VARCHAR(13000) NULL,
  `isEdited` TINYINT(1) NULL DEFAULT 0,
  `isDeleted` TINYINT(1) NULL DEFAULT 0,
  `isSpam` TINYINT(1) NULL DEFAULT 0,
  `isHighlighted` TINYINT(1) NULL DEFAULT 0,
  `isApproved` TINYINT(1) NULL DEFAULT 0,
  `forumShortName` VARCHAR(45) NULL,
  `points` INT NULL DEFAULT 0,
  `likes` INT NULL DEFAULT 0,
  `dislikes` INT NULL DEFAULT 0,
  PRIMARY KEY (`postId`),
  UNIQUE INDEX `postId_UNIQUE` (`postId` ASC),
  INDEX `fk_threadId_idx` (`threadId` ASC),
  INDEX `fk_parent_idx` (`parent` ASC),
  INDEX `fk_PostUserEmail_idx` (`userEmail` ASC),
  INDEX `fk_ForumShortName_idx` (`forumShortName` ASC),
  CONSTRAINT `fk_PostThreadId`
    FOREIGN KEY (`threadId`)
    REFERENCES `myForumApi`.`Thread` (`threadId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_PostUserEmail`
    FOREIGN KEY (`userEmail`)
    REFERENCES `myForumApi`.`User` (`email`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_PostParent`
    FOREIGN KEY (`parent`)
    REFERENCES `myForumApi`.`Post` (`postId`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ForumShortName`
    FOREIGN KEY (`forumShortName`)
    REFERENCES `myForumApi`.`Forum` (`shortName`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `myForumApi`.`Subscriber`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `myForumApi`.`Subscriber` (
  `userEmail` VARCHAR(45) NOT NULL,
  `threadId` INT NOT NULL,
  INDEX `fk_threadId_idx` (`threadId` ASC),
  PRIMARY KEY (`userEmail`, `threadId`),
  CONSTRAINT `fk_SubscriberUserEmail`
    FOREIGN KEY (`userEmail`)
    REFERENCES `myForumApi`.`User` (`email`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_SubscriberThreadId`
    FOREIGN KEY (`threadId`)
    REFERENCES `myForumApi`.`Thread` (`threadId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `myForumApi`.`Follower`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `myForumApi`.`Follower` (
  `followerEmail` VARCHAR(45) NOT NULL,
  `followeeEmail` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`followerEmail`, `followeeEmail`),
  CONSTRAINT `fk_FollowerFollowerEmail`
    FOREIGN KEY (`followerEmail`)
    REFERENCES `myForumApi`.`User` (`email`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_FollowerFolloweeEmail`
    FOREIGN KEY (`followeeEmail`)
    REFERENCES `myForumApi`.`User` (`email`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
