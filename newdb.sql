-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema myForumApi
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema myForumApi
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `myForumApi` DEFAULT CHARACTER SET utf8 ;
USE `myForumApi` ;

-- -----------------------------------------------------
-- Table `myForumApi`.`User`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `myForumApi`.`User` (
  `userId` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NULL DEFAULT NULL,
  `about` VARCHAR(5000) NULL DEFAULT NULL,
  `name` VARCHAR(45) NULL DEFAULT NULL,
  `email` VARCHAR(45) NOT NULL,
  `isAnonymous` TINYINT(1) NULL DEFAULT '0',
  PRIMARY KEY (`userId`, `email`),
  UNIQUE INDEX `user_id_UNIQUE` (`userId` ASC),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC),
  INDEX `email_name_userId` (`email` ASC, `name` ASC, `userId` ASC),
  INDEX `name_userId` (`name` ASC, `userId` ASC))
ENGINE = InnoDB
AUTO_INCREMENT = 102352
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `myForumApi`.`Follower`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `myForumApi`.`Follower` (
  `followerEmail` VARCHAR(45) NOT NULL,
  `followeeEmail` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`followerEmail`, `followeeEmail`),
  INDEX `user_getInfoUser` (`followeeEmail` ASC, `followerEmail` ASC),
  CONSTRAINT `fk_FollowerFolloweeEmail`
    FOREIGN KEY (`followeeEmail`)
    REFERENCES `myForumApi`.`User` (`email`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_FollowerFollowerEmail`
    FOREIGN KEY (`followerEmail`)
    REFERENCES `myForumApi`.`User` (`email`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `myForumApi`.`Forum`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `myForumApi`.`Forum` (
  `forumId` INT(11) NOT NULL AUTO_INCREMENT,
  `userEmail` VARCHAR(45) NULL DEFAULT NULL,
  `shortName` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`forumId`, `shortName`, `name`),
  UNIQUE INDEX `idForum_UNIQUE` (`forumId` ASC),
  UNIQUE INDEX `Forumcol_UNIQUE` (`shortName` ASC),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC),
  INDEX `fk_ForumUserEmail_idx` (`userEmail` ASC),
  INDEX `shortName_name_userEmail_forumId` (`shortName` ASC, `name` ASC, `userEmail` ASC, `forumId` ASC),
  CONSTRAINT `fk_ForumUserEmail`
    FOREIGN KEY (`userEmail`)
    REFERENCES `myForumApi`.`User` (`email`))
ENGINE = InnoDB
AUTO_INCREMENT = 1377
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `myForumApi`.`Thread`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `myForumApi`.`Thread` (
  `threadId` INT(11) NOT NULL AUTO_INCREMENT,
  `forumShortName` VARCHAR(45) NULL DEFAULT NULL,
  `userEmail` VARCHAR(45) NULL DEFAULT NULL,
  `title` VARCHAR(45) NULL DEFAULT NULL,
  `slug` VARCHAR(45) NULL DEFAULT NULL,
  `message` VARCHAR(4000) NULL DEFAULT NULL,
  `date` DATETIME NULL DEFAULT NULL,
  `isClosed` TINYINT(1) NULL DEFAULT '0',
  `isDeleted` TINYINT(1) NULL DEFAULT '0',
  `likes` INT(11) NULL DEFAULT '0',
  `dislikes` INT(11) NULL DEFAULT '0',
  `points` INT(11) NULL DEFAULT '0',
  `posts` INT(11) NULL DEFAULT 0,
  `allposts` INT(11) NULL DEFAULT 0,
  PRIMARY KEY (`threadId`),
  UNIQUE INDEX `threadId_UNIQUE` (`threadId` ASC),
  INDEX `fk_userId_idx` (`userEmail` ASC),
  INDEX `fk_forumId_idx` (`forumShortName` ASC),
  INDEX `userEmail_date_threadId` (`userEmail` ASC, `date` ASC, `threadId` ASC),
  INDEX `forumShortName_date_threadId` (`forumShortName` ASC, `date` ASC, `threadId` ASC),
  CONSTRAINT `fk_ThreadForumShortName`
    FOREIGN KEY (`forumShortName`)
    REFERENCES `myForumApi`.`Forum` (`shortName`),
  CONSTRAINT `fk_ThreadUserEmail`
    FOREIGN KEY (`userEmail`)
    REFERENCES `myForumApi`.`User` (`email`))
ENGINE = InnoDB
AUTO_INCREMENT = 11311
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `myForumApi`.`Post`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `myForumApi`.`Post` (
  `postId` INT(11) NOT NULL AUTO_INCREMENT,
  `threadId` INT(11) NULL DEFAULT NULL,
  `userEmail` VARCHAR(45) NULL DEFAULT NULL,
  `parent` INT(11) NULL DEFAULT NULL,
  `datePost` DATETIME NULL DEFAULT NULL,
  `message` VARCHAR(13000) NULL DEFAULT NULL,
  `isEdited` TINYINT(1) NULL DEFAULT '0',
  `isDeleted` TINYINT(1) NULL DEFAULT '0',
  `isSpam` TINYINT(1) NULL DEFAULT '0',
  `isHighlighted` TINYINT(1) NULL DEFAULT '0',
  `isApproved` TINYINT(1) NULL DEFAULT '0',
  `forumShortName` VARCHAR(45) NULL DEFAULT NULL,
  `likes` INT(11) NULL DEFAULT '0',
  `dislikes` INT(11) NULL DEFAULT '0',
  PRIMARY KEY (`postId`),
  UNIQUE INDEX `postId_UNIQUE` (`postId` ASC),
  INDEX `fk_threadId_idx` (`threadId` ASC),
  INDEX `fk_parent_idx` (`parent` ASC),
  INDEX `fk_PostUserEmail_idx` (`userEmail` ASC),
  INDEX `fk_ForumShortName_idx` (`forumShortName` ASC),
  INDEX `forumShortName_datePost_postId` (`forumShortName` ASC, `datePost` ASC, `postId` ASC),
  INDEX `threadId_datePost_postId` (`threadId` ASC, `datePost` ASC, `postId` ASC),
  INDEX `userEmail_datePost_postId` (`userEmail` ASC, `datePost` ASC, `postId` ASC),
  INDEX `forumShortName_userEmail` (`forumShortName` ASC, `userEmail` ASC),
  INDEX `postId_threadId` (`postId` ASC, `threadId` ASC),
  CONSTRAINT `fk_ForumShortName`
    FOREIGN KEY (`forumShortName`)
    REFERENCES `myForumApi`.`Forum` (`shortName`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_PostParent`
    FOREIGN KEY (`parent`)
    REFERENCES `myForumApi`.`Post` (`postId`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_PostThreadId`
    FOREIGN KEY (`threadId`)
    REFERENCES `myForumApi`.`Thread` (`threadId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_PostUserEmail`
    FOREIGN KEY (`userEmail`)
    REFERENCES `myForumApi`.`User` (`email`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 104571
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `myForumApi`.`Subscriber`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `myForumApi`.`Subscriber` (
  `userEmail` VARCHAR(45) NOT NULL,
  `threadId` INT(11) NOT NULL,
  PRIMARY KEY (`userEmail`, `threadId`),
  INDEX `user_getInfoUser` (`threadId` ASC, `userEmail` ASC),
  CONSTRAINT `fk_SubscriberThreadId`
    FOREIGN KEY (`threadId`)
    REFERENCES `myForumApi`.`Thread` (`threadId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_SubscriberUserEmail`
    FOREIGN KEY (`userEmail`)
    REFERENCES `myForumApi`.`User` (`email`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
