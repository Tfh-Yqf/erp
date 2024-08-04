CREATE DATABASE IF NOT EXISTS erp_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'root'@'localhost' IDENTIFIED BY 'ERPSYSTE';
GRANT ALL PRIVILEGES ON erp_db.* TO 'root'@'localhost';
FLUSH PRIVILEGES;


/*
 Navicat Premium Data Transfer

 Source Server         : erp
 Source Server Type    : MySQL
 Source Server Version : 80013
 Source Host           : tanfuhua.mysql.polardb.rds.aliyuncs.com:3306
 Source Schema         : erp_db

 Target Server Type    : MySQL
 Target Server Version : 80013
 File Encoding         : 65001

 Date: 03/08/2024 21:47:38
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
                               `id` int(11) NOT NULL AUTO_INCREMENT,
                               `name` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                               PRIMARY KEY (`id`) USING BTREE,
                               UNIQUE INDEX `name`(`name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of auth_group
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
                                           `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                           `group_id` int(11) NOT NULL,
                                           `permission_id` int(11) NOT NULL,
                                           PRIMARY KEY (`id`) USING BTREE,
                                           UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id` ASC, `permission_id` ASC) USING BTREE,
                                           INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id` ASC) USING BTREE,
                                           CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                           CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
                                    `id` int(11) NOT NULL AUTO_INCREMENT,
                                    `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                    `content_type_id` int(11) NOT NULL,
                                    `codename` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                    PRIMARY KEY (`id`) USING BTREE,
                                    UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id` ASC, `codename` ASC) USING BTREE,
                                    CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 233 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------

-- ----------------------------
-- Table structure for data_account
-- ----------------------------
DROP TABLE IF EXISTS `data_account`;
CREATE TABLE `data_account`  (
                                 `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                 `number` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                 `name` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                 `type` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                 `holder` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                 `card_number` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                 `remark` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                 `is_active` tinyint(1) NOT NULL,
                                 `initial_balance_amount` decimal(16, 2) NOT NULL,
                                 `balance_amount` decimal(16, 2) NOT NULL,
                                 `has_balance` tinyint(1) NOT NULL,
                                 `team_id` bigint(20) NOT NULL,
                                 PRIMARY KEY (`id`) USING BTREE,
                                 UNIQUE INDEX `data_account_number_team_id_f5280378_uniq`(`number` ASC, `team_id` ASC) USING BTREE,
                                 UNIQUE INDEX `data_account_name_team_id_b5b809ce_uniq`(`name` ASC, `team_id` ASC) USING BTREE,
                                 INDEX `data_account_team_id_9f2c5d33_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                 CONSTRAINT `data_account_team_id_9f2c5d33_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of data_account
-- ----------------------------
INSERT INTO `data_account` VALUES (6, 'A001', 'ww', 'wechat', NULL, NULL, NULL, 1, 0.00, 0.00, 0, 5);
INSERT INTO `data_account` VALUES (7, 'A002', 'wjj1', 'cash', NULL, NULL, NULL, 1, 0.00, 0.00, 0, 5);
INSERT INTO `data_account` VALUES (8, 'A003', 'yh', 'cash', NULL, NULL, NULL, 1, 0.00, 0.00, 0, 5);
INSERT INTO `data_account` VALUES (9, 'A004', 'admin', 'other', NULL, NULL, NULL, 1, 0.00, 0.00, 0, 5);
INSERT INTO `data_account` VALUES (10, 'A001', '默认账户', 'cash', NULL, NULL, NULL, 1, 0.00, 0.00, 0, 3);

-- ----------------------------
-- Table structure for data_chargeitem
-- ----------------------------
DROP TABLE IF EXISTS `data_chargeitem`;
CREATE TABLE `data_chargeitem`  (
                                    `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                    `name` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                    `type` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                    `remark` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                    `team_id` bigint(20) NOT NULL,
                                    PRIMARY KEY (`id`) USING BTREE,
                                    UNIQUE INDEX `data_chargeitem_name_team_id_9f8d9964_uniq`(`name` ASC, `team_id` ASC) USING BTREE,
                                    INDEX `data_chargeitem_team_id_89601413_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                    CONSTRAINT `data_chargeitem_team_id_89601413_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of data_chargeitem
-- ----------------------------

-- ----------------------------
-- Table structure for data_client
-- ----------------------------
DROP TABLE IF EXISTS `data_client`;
CREATE TABLE `data_client`  (
                                `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                `number` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                `name` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                `level` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                `contact` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                `phone` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                `email` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                `address` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                `remark` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                `is_active` tinyint(1) NOT NULL,
                                `initial_arrears_amount` decimal(16, 2) NOT NULL,
                                `arrears_amount` decimal(16, 2) NOT NULL,
                                `has_arrears` tinyint(1) NOT NULL,
                                `team_id` bigint(20) NOT NULL,
                                PRIMARY KEY (`id`) USING BTREE,
                                UNIQUE INDEX `data_client_number_team_id_629bed39_uniq`(`number` ASC, `team_id` ASC) USING BTREE,
                                UNIQUE INDEX `data_client_name_team_id_eb5af604_uniq`(`name` ASC, `team_id` ASC) USING BTREE,
                                INDEX `data_client_team_id_6c2006de_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                CONSTRAINT `data_client_team_id_6c2006de_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of data_client
-- ----------------------------
INSERT INTO `data_client` VALUES (4, 'C001', '客户1', '0', NULL, NULL, NULL, NULL, NULL, 0, 0.00, 8632.47, 1, 5);
INSERT INTO `data_client` VALUES (5, 'C002', '闲鱼客户', '0', NULL, NULL, NULL, NULL, NULL, 1, 0.00, 1.01, 1, 5);
INSERT INTO `data_client` VALUES (7, 'C003', 'sss', '0', NULL, NULL, NULL, NULL, NULL, 1, 0.00, 0.00, 0, 5);
INSERT INTO `data_client` VALUES (8, 'C004', '实时', '0', NULL, NULL, NULL, NULL, NULL, 1, 0.00, 0.00, 0, 5);
INSERT INTO `data_client` VALUES (9, 'C005', '张小龙', '0', NULL, NULL, NULL, NULL, 'hhh', 1, 10000.00, 10000.00, 1, 5);
INSERT INTO `data_client` VALUES (11, 'C001', '默认客户', '0', NULL, NULL, NULL, NULL, NULL, 1, 0.00, 0.00, 0, 3);

-- ----------------------------
-- Table structure for data_supplier
-- ----------------------------
DROP TABLE IF EXISTS `data_supplier`;
CREATE TABLE `data_supplier`  (
                                  `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                  `number` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                  `name` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                  `contact` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                  `phone` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                  `email` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                  `address` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                  `bank_account` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                  `bank_name` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                  `remark` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                  `is_active` tinyint(1) NOT NULL,
                                  `initial_arrears_amount` decimal(16, 2) NOT NULL,
                                  `arrears_amount` decimal(16, 2) NOT NULL,
                                  `has_arrears` tinyint(1) NOT NULL,
                                  `team_id` bigint(20) NOT NULL,
                                  PRIMARY KEY (`id`) USING BTREE,
                                  UNIQUE INDEX `data_supplier_number_team_id_1030751c_uniq`(`number` ASC, `team_id` ASC) USING BTREE,
                                  UNIQUE INDEX `data_supplier_name_team_id_5a492eed_uniq`(`name` ASC, `team_id` ASC) USING BTREE,
                                  INDEX `data_supplier_team_id_0891404f_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                  CONSTRAINT `data_supplier_team_id_0891404f_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of data_supplier
-- ----------------------------
INSERT INTO `data_supplier` VALUES (4, 'S001', '供应商1', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 0.00, 15735.00, 1, 5);
INSERT INTO `data_supplier` VALUES (5, 'S002', 'S002', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 0.00, 33000.00, 1, 5);
INSERT INTO `data_supplier` VALUES (6, 'S003', '罗腾龙', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 0.00, 0.00, 0, 5);
INSERT INTO `data_supplier` VALUES (7, 'S004', 'LL001', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 0.00, 9900.00, 1, 5);
INSERT INTO `data_supplier` VALUES (8, 'S001', '默认供应商', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 0.00, 0.00, 0, 3);

-- ----------------------------
-- Table structure for data_warehouse
-- ----------------------------
DROP TABLE IF EXISTS `data_warehouse`;
CREATE TABLE `data_warehouse`  (
                                   `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                   `number` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                   `name` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                   `phone` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                   `address` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                   `remark` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                   `is_active` tinyint(1) NOT NULL,
                                   `manager_id` bigint(20) NULL DEFAULT NULL,
                                   `team_id` bigint(20) NOT NULL,
                                   PRIMARY KEY (`id`) USING BTREE,
                                   UNIQUE INDEX `data_warehouse_number_team_id_28af4b59_uniq`(`number` ASC, `team_id` ASC) USING BTREE,
                                   UNIQUE INDEX `data_warehouse_name_team_id_5a0d0bbd_uniq`(`name` ASC, `team_id` ASC) USING BTREE,
                                   INDEX `data_warehouse_manager_id_f0be739c_fk_system_user_id`(`manager_id` ASC) USING BTREE,
                                   INDEX `data_warehouse_team_id_bd2a149a_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                   CONSTRAINT `data_warehouse_manager_id_f0be739c_fk_system_user_id` FOREIGN KEY (`manager_id`) REFERENCES `system_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                   CONSTRAINT `data_warehouse_team_id_bd2a149a_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of data_warehouse
-- ----------------------------
INSERT INTO `data_warehouse` VALUES (4, 'W001', '仓库1', NULL, NULL, NULL, 1, NULL, 5);
INSERT INTO `data_warehouse` VALUES (6, 'W002', '仓库2', NULL, NULL, NULL, 0, 6, 5);
INSERT INTO `data_warehouse` VALUES (7, 'W001', '默认仓库', NULL, NULL, NULL, 1, NULL, 3);

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log`  (
                                     `id` int(11) NOT NULL AUTO_INCREMENT,
                                     `action_time` datetime(6) NOT NULL,
                                     `object_id` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
                                     `object_repr` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                     `action_flag` smallint(5) UNSIGNED NOT NULL,
                                     `change_message` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                     `content_type_id` int(11) NULL DEFAULT NULL,
                                     `user_id` bigint(20) NOT NULL,
                                     PRIMARY KEY (`id`) USING BTREE,
                                     INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co`(`content_type_id` ASC) USING BTREE,
                                     INDEX `django_admin_log_user_id_c564eba6_fk_manage_superuser_id`(`user_id` ASC) USING BTREE,
                                     CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                     CONSTRAINT `django_admin_log_user_id_c564eba6_fk_manage_superuser_id` FOREIGN KEY (`user_id`) REFERENCES `manage_superuser` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
                                        `id` int(11) NOT NULL AUTO_INCREMENT,
                                        `app_label` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                        `model` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                        PRIMARY KEY (`id`) USING BTREE,
                                        UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label` ASC, `model` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 59 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
                                      `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                      `app` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                      `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                      `applied` datetime(6) NOT NULL,
                                      PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 32 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
                                   `session_key` varchar(40) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                   `session_data` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                   `expire_date` datetime(6) NOT NULL,
                                   PRIMARY KEY (`session_key`) USING BTREE,
                                   INDEX `django_session_expire_date_a5c62663`(`expire_date` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of django_session
-- ----------------------------

-- ----------------------------
-- Table structure for finance_accounttransferrecord
-- ----------------------------
DROP TABLE IF EXISTS `finance_accounttransferrecord`;
CREATE TABLE `finance_accounttransferrecord`  (
                                                  `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                                  `transfer_out_time` datetime(6) NOT NULL,
                                                  `transfer_in_time` datetime(6) NOT NULL,
                                                  `transfer_amount` decimal(16, 2) NOT NULL,
                                                  `service_charge_amount` decimal(16, 2) NOT NULL,
                                                  `service_charge_payer` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                                  `handle_time` date NOT NULL,
                                                  `remark` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                                  `is_void` tinyint(1) NOT NULL,
                                                  `create_time` datetime(6) NOT NULL,
                                                  `creator_id` bigint(20) NOT NULL,
                                                  `handler_id` bigint(20) NOT NULL,
                                                  `in_account_id` bigint(20) NOT NULL,
                                                  `out_account_id` bigint(20) NOT NULL,
                                                  `team_id` bigint(20) NOT NULL,
                                                  PRIMARY KEY (`id`) USING BTREE,
                                                  INDEX `finance_accounttrans_creator_id_fb7d0093_fk_system_us`(`creator_id` ASC) USING BTREE,
                                                  INDEX `finance_accounttrans_handler_id_2cb85684_fk_system_us`(`handler_id` ASC) USING BTREE,
                                                  INDEX `finance_accounttrans_in_account_id_64f686b7_fk_data_acco`(`in_account_id` ASC) USING BTREE,
                                                  INDEX `finance_accounttrans_out_account_id_c687221e_fk_data_acco`(`out_account_id` ASC) USING BTREE,
                                                  INDEX `finance_accounttransferrecord_team_id_097367c2_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                                  CONSTRAINT `finance_accounttrans_creator_id_fb7d0093_fk_system_us` FOREIGN KEY (`creator_id`) REFERENCES `system_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                  CONSTRAINT `finance_accounttrans_handler_id_2cb85684_fk_system_us` FOREIGN KEY (`handler_id`) REFERENCES `system_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                  CONSTRAINT `finance_accounttrans_in_account_id_64f686b7_fk_data_acco` FOREIGN KEY (`in_account_id`) REFERENCES `data_account` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                  CONSTRAINT `finance_accounttrans_out_account_id_c687221e_fk_data_acco` FOREIGN KEY (`out_account_id`) REFERENCES `data_account` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                  CONSTRAINT `finance_accounttransferrecord_team_id_097367c2_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of finance_accounttransferrecord
-- ----------------------------

-- ----------------------------
-- Table structure for finance_chargeorder
-- ----------------------------
DROP TABLE IF EXISTS `finance_chargeorder`;
CREATE TABLE `finance_chargeorder`  (
                                        `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                        `number` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                        `type` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                        `handle_time` date NOT NULL,
                                        `charge_item_name` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                        `total_amount` decimal(16, 2) NOT NULL,
                                        `charge_amount` decimal(16, 2) NOT NULL,
                                        `remark` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                        `is_void` tinyint(1) NOT NULL,
                                        `create_time` datetime(6) NOT NULL,
                                        `account_id` bigint(20) NOT NULL,
                                        `charge_item_id` bigint(20) NULL DEFAULT NULL,
                                        `client_id` bigint(20) NULL DEFAULT NULL,
                                        `creator_id` bigint(20) NOT NULL,
                                        `handler_id` bigint(20) NOT NULL,
                                        `supplier_id` bigint(20) NULL DEFAULT NULL,
                                        `team_id` bigint(20) NOT NULL,
                                        PRIMARY KEY (`id`) USING BTREE,
                                        UNIQUE INDEX `finance_chargeorder_number_team_id_bcb2c2f9_uniq`(`number` ASC, `team_id` ASC) USING BTREE,
                                        INDEX `finance_chargeorder_account_id_2dd7cfcd_fk_data_account_id`(`account_id` ASC) USING BTREE,
                                        INDEX `finance_chargeorder_charge_item_id_e48fd925_fk_data_char`(`charge_item_id` ASC) USING BTREE,
                                        INDEX `finance_chargeorder_client_id_e11b2275_fk_data_client_id`(`client_id` ASC) USING BTREE,
                                        INDEX `finance_chargeorder_creator_id_4229838f_fk_system_user_id`(`creator_id` ASC) USING BTREE,
                                        INDEX `finance_chargeorder_handler_id_eab046f6_fk_system_user_id`(`handler_id` ASC) USING BTREE,
                                        INDEX `finance_chargeorder_supplier_id_c5b95ba4_fk_data_supplier_id`(`supplier_id` ASC) USING BTREE,
                                        INDEX `finance_chargeorder_team_id_2b1ce1c7_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                        CONSTRAINT `finance_chargeorder_account_id_2dd7cfcd_fk_data_account_id` FOREIGN KEY (`account_id`) REFERENCES `data_account` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                        CONSTRAINT `finance_chargeorder_charge_item_id_e48fd925_fk_data_char` FOREIGN KEY (`charge_item_id`) REFERENCES `data_chargeitem` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                        CONSTRAINT `finance_chargeorder_client_id_e11b2275_fk_data_client_id` FOREIGN KEY (`client_id`) REFERENCES `data_client` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                        CONSTRAINT `finance_chargeorder_creator_id_4229838f_fk_system_user_id` FOREIGN KEY (`creator_id`) REFERENCES `system_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                        CONSTRAINT `finance_chargeorder_handler_id_eab046f6_fk_system_user_id` FOREIGN KEY (`handler_id`) REFERENCES `system_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                        CONSTRAINT `finance_chargeorder_supplier_id_c5b95ba4_fk_data_supplier_id` FOREIGN KEY (`supplier_id`) REFERENCES `data_supplier` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                        CONSTRAINT `finance_chargeorder_team_id_2b1ce1c7_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of finance_chargeorder
-- ----------------------------

-- ----------------------------
-- Table structure for finance_collectionaccount
-- ----------------------------
DROP TABLE IF EXISTS `finance_collectionaccount`;
CREATE TABLE `finance_collectionaccount`  (
                                              `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                              `collection_amount` decimal(16, 2) NOT NULL,
                                              `account_id` bigint(20) NOT NULL,
                                              `collection_order_id` bigint(20) NOT NULL,
                                              `team_id` bigint(20) NOT NULL,
                                              PRIMARY KEY (`id`) USING BTREE,
                                              UNIQUE INDEX `finance_collectionaccoun_collection_order_id_acco_be79096e_uniq`(`collection_order_id` ASC, `account_id` ASC) USING BTREE,
                                              INDEX `finance_collectionaccount_account_id_ada2b1c0_fk_data_account_id`(`account_id` ASC) USING BTREE,
                                              INDEX `finance_collectionaccount_team_id_5885f8a8_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                              CONSTRAINT `finance_collectionac_collection_order_id_d58d9391_fk_finance_c` FOREIGN KEY (`collection_order_id`) REFERENCES `finance_collectionorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                              CONSTRAINT `finance_collectionaccount_account_id_ada2b1c0_fk_data_account_id` FOREIGN KEY (`account_id`) REFERENCES `data_account` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                              CONSTRAINT `finance_collectionaccount_team_id_5885f8a8_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of finance_collectionaccount
-- ----------------------------
INSERT INTO `finance_collectionaccount` VALUES (3, 88.00, 8, 3, 5);
INSERT INTO `finance_collectionaccount` VALUES (4, 88.00, 7, 3, 5);

-- ----------------------------
-- Table structure for finance_collectionorder
-- ----------------------------
DROP TABLE IF EXISTS `finance_collectionorder`;
CREATE TABLE `finance_collectionorder`  (
                                            `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                            `number` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                            `handle_time` date NOT NULL,
                                            `remark` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                            `total_amount` decimal(16, 2) NULL DEFAULT NULL,
                                            `discount_amount` decimal(16, 2) NOT NULL,
                                            `is_void` tinyint(1) NOT NULL,
                                            `create_time` datetime(6) NOT NULL,
                                            `client_id` bigint(20) NOT NULL,
                                            `creator_id` bigint(20) NOT NULL,
                                            `handler_id` bigint(20) NOT NULL,
                                            `team_id` bigint(20) NOT NULL,
                                            PRIMARY KEY (`id`) USING BTREE,
                                            UNIQUE INDEX `finance_collectionorder_number_team_id_553af3f6_uniq`(`number` ASC, `team_id` ASC) USING BTREE,
                                            INDEX `finance_collectionorder_client_id_755ba0a5_fk_data_client_id`(`client_id` ASC) USING BTREE,
                                            INDEX `finance_collectionorder_creator_id_3c177d59_fk_system_user_id`(`creator_id` ASC) USING BTREE,
                                            INDEX `finance_collectionorder_handler_id_424884bd_fk_system_user_id`(`handler_id` ASC) USING BTREE,
                                            INDEX `finance_collectionorder_team_id_07fe61ff_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                            CONSTRAINT `finance_collectionorder_client_id_755ba0a5_fk_data_client_id` FOREIGN KEY (`client_id`) REFERENCES `data_client` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                            CONSTRAINT `finance_collectionorder_creator_id_3c177d59_fk_system_user_id` FOREIGN KEY (`creator_id`) REFERENCES `system_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                            CONSTRAINT `finance_collectionorder_handler_id_424884bd_fk_system_user_id` FOREIGN KEY (`handler_id`) REFERENCES `system_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                            CONSTRAINT `finance_collectionorder_team_id_07fe61ff_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of finance_collectionorder
-- ----------------------------
INSERT INTO `finance_collectionorder` VALUES (3, 'SK202406300001', '2024-06-08', NULL, 176.00, 0.00, 1, '2024-06-30 14:58:56.168035', 5, 6, 7, 5);

-- ----------------------------
-- Table structure for finance_paymentaccount
-- ----------------------------
DROP TABLE IF EXISTS `finance_paymentaccount`;
CREATE TABLE `finance_paymentaccount`  (
                                           `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                           `payment_amount` decimal(16, 2) NOT NULL,
                                           `account_id` bigint(20) NOT NULL,
                                           `payment_order_id` bigint(20) NOT NULL,
                                           `team_id` bigint(20) NOT NULL,
                                           PRIMARY KEY (`id`) USING BTREE,
                                           UNIQUE INDEX `finance_paymentaccount_payment_order_id_account_id_2954299c_uniq`(`payment_order_id` ASC, `account_id` ASC) USING BTREE,
                                           INDEX `finance_paymentaccount_account_id_2d437170_fk_data_account_id`(`account_id` ASC) USING BTREE,
                                           INDEX `finance_paymentaccount_team_id_c5ee4531_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                           CONSTRAINT `finance_paymentaccou_payment_order_id_9177ae4f_fk_finance_p` FOREIGN KEY (`payment_order_id`) REFERENCES `finance_paymentorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                           CONSTRAINT `finance_paymentaccount_account_id_2d437170_fk_data_account_id` FOREIGN KEY (`account_id`) REFERENCES `data_account` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                           CONSTRAINT `finance_paymentaccount_team_id_c5ee4531_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of finance_paymentaccount
-- ----------------------------

-- ----------------------------
-- Table structure for finance_paymentorder
-- ----------------------------
DROP TABLE IF EXISTS `finance_paymentorder`;
CREATE TABLE `finance_paymentorder`  (
                                         `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                         `number` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                         `handle_time` date NOT NULL,
                                         `remark` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                         `total_amount` decimal(16, 2) NULL DEFAULT NULL,
                                         `discount_amount` decimal(16, 2) NOT NULL,
                                         `is_void` tinyint(1) NOT NULL,
                                         `create_time` datetime(6) NOT NULL,
                                         `creator_id` bigint(20) NOT NULL,
                                         `handler_id` bigint(20) NOT NULL,
                                         `supplier_id` bigint(20) NOT NULL,
                                         `team_id` bigint(20) NOT NULL,
                                         PRIMARY KEY (`id`) USING BTREE,
                                         UNIQUE INDEX `finance_paymentorder_number_team_id_31e75e72_uniq`(`number` ASC, `team_id` ASC) USING BTREE,
                                         INDEX `finance_paymentorder_creator_id_47fee2e7_fk_system_user_id`(`creator_id` ASC) USING BTREE,
                                         INDEX `finance_paymentorder_handler_id_1467ebc0_fk_system_user_id`(`handler_id` ASC) USING BTREE,
                                         INDEX `finance_paymentorder_supplier_id_925ee064_fk_data_supplier_id`(`supplier_id` ASC) USING BTREE,
                                         INDEX `finance_paymentorder_team_id_26f5375f_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                         CONSTRAINT `finance_paymentorder_creator_id_47fee2e7_fk_system_user_id` FOREIGN KEY (`creator_id`) REFERENCES `system_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                         CONSTRAINT `finance_paymentorder_handler_id_1467ebc0_fk_system_user_id` FOREIGN KEY (`handler_id`) REFERENCES `system_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                         CONSTRAINT `finance_paymentorder_supplier_id_925ee064_fk_data_supplier_id` FOREIGN KEY (`supplier_id`) REFERENCES `data_supplier` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                         CONSTRAINT `finance_paymentorder_team_id_26f5375f_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of finance_paymentorder
-- ----------------------------

-- ----------------------------
-- Table structure for flow_financeflow
-- ----------------------------
DROP TABLE IF EXISTS `flow_financeflow`;
CREATE TABLE `flow_financeflow`  (
                                     `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                     `type` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                     `amount_before` double NOT NULL,
                                     `amount_change` double NOT NULL,
                                     `amount_after` double NOT NULL,
                                     `create_time` datetime(6) NOT NULL,
                                     `account_id` bigint(20) NOT NULL,
                                     `account_transfer_record_id` bigint(20) NULL DEFAULT NULL,
                                     `charge_order_id` bigint(20) NULL DEFAULT NULL,
                                     `collection_order_id` bigint(20) NULL DEFAULT NULL,
                                     `creator_id` bigint(20) NULL DEFAULT NULL,
                                     `payment_order_id` bigint(20) NULL DEFAULT NULL,
                                     `purchase_order_id` bigint(20) NULL DEFAULT NULL,
                                     `purchase_return_order_id` bigint(20) NULL DEFAULT NULL,
                                     `sales_order_id` bigint(20) NULL DEFAULT NULL,
                                     `sales_return_order_id` bigint(20) NULL DEFAULT NULL,
                                     `team_id` bigint(20) NOT NULL,
                                     `void_account_transfer_record_id` bigint(20) NULL DEFAULT NULL,
                                     `void_charge_order_id` bigint(20) NULL DEFAULT NULL,
                                     `void_collection_order_id` bigint(20) NULL DEFAULT NULL,
                                     `void_payment_order_id` bigint(20) NULL DEFAULT NULL,
                                     `void_purchase_order_id` bigint(20) NULL DEFAULT NULL,
                                     `void_purchase_return_order_id` bigint(20) NULL DEFAULT NULL,
                                     `void_sales_order_id` bigint(20) NULL DEFAULT NULL,
                                     `void_sales_return_order_id` bigint(20) NULL DEFAULT NULL,
                                     PRIMARY KEY (`id`) USING BTREE,
                                     INDEX `flow_financeflow_account_id_284faa7a_fk_data_account_id`(`account_id` ASC) USING BTREE,
                                     INDEX `flow_financeflow_account_transfer_rec_5262459e_fk_finance_a`(`account_transfer_record_id` ASC) USING BTREE,
                                     INDEX `flow_financeflow_charge_order_id_f40d9dd7_fk_finance_c`(`charge_order_id` ASC) USING BTREE,
                                     INDEX `flow_financeflow_collection_order_id_9a88e241_fk_finance_c`(`collection_order_id` ASC) USING BTREE,
                                     INDEX `flow_financeflow_creator_id_d4aa65b9_fk_system_user_id`(`creator_id` ASC) USING BTREE,
                                     INDEX `flow_financeflow_payment_order_id_7290302a_fk_finance_p`(`payment_order_id` ASC) USING BTREE,
                                     INDEX `flow_financeflow_purchase_order_id_c0b7eac5_fk_purchase_`(`purchase_order_id` ASC) USING BTREE,
                                     INDEX `flow_financeflow_purchase_return_orde_57faacdd_fk_purchase_`(`purchase_return_order_id` ASC) USING BTREE,
                                     INDEX `flow_financeflow_sales_order_id_190089c4_fk_sales_salesorder_id`(`sales_order_id` ASC) USING BTREE,
                                     INDEX `flow_financeflow_sales_return_order_i_75fd9b57_fk_sales_sal`(`sales_return_order_id` ASC) USING BTREE,
                                     INDEX `flow_financeflow_team_id_941541e6_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                     INDEX `flow_financeflow_void_account_transfe_f4ed1867_fk_finance_a`(`void_account_transfer_record_id` ASC) USING BTREE,
                                     INDEX `flow_financeflow_void_charge_order_id_5292f89a_fk_finance_c`(`void_charge_order_id` ASC) USING BTREE,
                                     INDEX `flow_financeflow_void_collection_orde_a88a4e48_fk_finance_c`(`void_collection_order_id` ASC) USING BTREE,
                                     INDEX `flow_financeflow_void_payment_order_i_3687226b_fk_finance_p`(`void_payment_order_id` ASC) USING BTREE,
                                     INDEX `flow_financeflow_void_purchase_order__db3d8d02_fk_purchase_`(`void_purchase_order_id` ASC) USING BTREE,
                                     INDEX `flow_financeflow_void_purchase_return_2f432074_fk_purchase_`(`void_purchase_return_order_id` ASC) USING BTREE,
                                     INDEX `flow_financeflow_void_sales_order_id_6c125138_fk_sales_sal`(`void_sales_order_id` ASC) USING BTREE,
                                     INDEX `flow_financeflow_void_sales_return_or_01b815f6_fk_sales_sal`(`void_sales_return_order_id` ASC) USING BTREE,
                                     CONSTRAINT `flow_financeflow_account_id_284faa7a_fk_data_account_id` FOREIGN KEY (`account_id`) REFERENCES `data_account` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                     CONSTRAINT `flow_financeflow_account_transfer_rec_5262459e_fk_finance_a` FOREIGN KEY (`account_transfer_record_id`) REFERENCES `finance_accounttransferrecord` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                     CONSTRAINT `flow_financeflow_charge_order_id_f40d9dd7_fk_finance_c` FOREIGN KEY (`charge_order_id`) REFERENCES `finance_chargeorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                     CONSTRAINT `flow_financeflow_collection_order_id_9a88e241_fk_finance_c` FOREIGN KEY (`collection_order_id`) REFERENCES `finance_collectionorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                     CONSTRAINT `flow_financeflow_creator_id_d4aa65b9_fk_system_user_id` FOREIGN KEY (`creator_id`) REFERENCES `system_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                     CONSTRAINT `flow_financeflow_payment_order_id_7290302a_fk_finance_p` FOREIGN KEY (`payment_order_id`) REFERENCES `finance_paymentorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                     CONSTRAINT `flow_financeflow_purchase_order_id_c0b7eac5_fk_purchase_` FOREIGN KEY (`purchase_order_id`) REFERENCES `purchase_purchaseorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                     CONSTRAINT `flow_financeflow_purchase_return_orde_57faacdd_fk_purchase_` FOREIGN KEY (`purchase_return_order_id`) REFERENCES `purchase_purchasereturnorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                     CONSTRAINT `flow_financeflow_sales_order_id_190089c4_fk_sales_salesorder_id` FOREIGN KEY (`sales_order_id`) REFERENCES `sales_salesorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                     CONSTRAINT `flow_financeflow_sales_return_order_i_75fd9b57_fk_sales_sal` FOREIGN KEY (`sales_return_order_id`) REFERENCES `sales_salesreturnorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                     CONSTRAINT `flow_financeflow_team_id_941541e6_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                     CONSTRAINT `flow_financeflow_void_account_transfe_f4ed1867_fk_finance_a` FOREIGN KEY (`void_account_transfer_record_id`) REFERENCES `finance_accounttransferrecord` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                     CONSTRAINT `flow_financeflow_void_charge_order_id_5292f89a_fk_finance_c` FOREIGN KEY (`void_charge_order_id`) REFERENCES `finance_chargeorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                     CONSTRAINT `flow_financeflow_void_collection_orde_a88a4e48_fk_finance_c` FOREIGN KEY (`void_collection_order_id`) REFERENCES `finance_collectionorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                     CONSTRAINT `flow_financeflow_void_payment_order_i_3687226b_fk_finance_p` FOREIGN KEY (`void_payment_order_id`) REFERENCES `finance_paymentorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                     CONSTRAINT `flow_financeflow_void_purchase_order__db3d8d02_fk_purchase_` FOREIGN KEY (`void_purchase_order_id`) REFERENCES `purchase_purchaseorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                     CONSTRAINT `flow_financeflow_void_purchase_return_2f432074_fk_purchase_` FOREIGN KEY (`void_purchase_return_order_id`) REFERENCES `purchase_purchasereturnorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                     CONSTRAINT `flow_financeflow_void_sales_order_id_6c125138_fk_sales_sal` FOREIGN KEY (`void_sales_order_id`) REFERENCES `sales_salesorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                     CONSTRAINT `flow_financeflow_void_sales_return_or_01b815f6_fk_sales_sal` FOREIGN KEY (`void_sales_return_order_id`) REFERENCES `sales_salesreturnorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 17 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of flow_financeflow
-- ----------------------------
INSERT INTO `flow_financeflow` VALUES (13, 'collection', 0, 88, 88, '2024-06-30 14:58:56.554867', 7, NULL, NULL, 3, 6, NULL, NULL, NULL, NULL, NULL, 5, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `flow_financeflow` VALUES (14, 'collection', 0, 88, 88, '2024-06-30 14:58:56.554956', 8, NULL, NULL, 3, 6, NULL, NULL, NULL, NULL, NULL, 5, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `flow_financeflow` VALUES (15, 'void_collection', 88, 88, 0, '2024-06-30 15:11:56.635148', 7, NULL, NULL, NULL, 6, NULL, NULL, NULL, NULL, NULL, 5, NULL, NULL, 3, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `flow_financeflow` VALUES (16, 'void_collection', 88, 88, 0, '2024-06-30 15:11:56.635264', 8, NULL, NULL, NULL, 6, NULL, NULL, NULL, NULL, NULL, 5, NULL, NULL, 3, NULL, NULL, NULL, NULL, NULL);

-- ----------------------------
-- Table structure for flow_inventoryflow
-- ----------------------------
DROP TABLE IF EXISTS `flow_inventoryflow`;
CREATE TABLE `flow_inventoryflow`  (
                                       `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                       `type` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                       `quantity_before` double NOT NULL,
                                       `quantity_change` double NOT NULL,
                                       `quantity_after` double NOT NULL,
                                       `create_time` datetime(6) NOT NULL,
                                       `creator_id` bigint(20) NOT NULL,
                                       `goods_id` bigint(20) NOT NULL,
                                       `purchase_order_id` bigint(20) NULL DEFAULT NULL,
                                       `purchase_return_order_id` bigint(20) NULL DEFAULT NULL,
                                       `sales_order_id` bigint(20) NULL DEFAULT NULL,
                                       `sales_return_order_id` bigint(20) NULL DEFAULT NULL,
                                       `stock_check_order_id` bigint(20) NULL DEFAULT NULL,
                                       `stock_in_order_id` bigint(20) NULL DEFAULT NULL,
                                       `stock_out_order_id` bigint(20) NULL DEFAULT NULL,
                                       `stock_transfer_order_id` bigint(20) NULL DEFAULT NULL,
                                       `team_id` bigint(20) NOT NULL,
                                       `void_purchase_order_id` bigint(20) NULL DEFAULT NULL,
                                       `void_purchase_return_order_id` bigint(20) NULL DEFAULT NULL,
                                       `void_sales_order_id` bigint(20) NULL DEFAULT NULL,
                                       `void_sales_return_order_id` bigint(20) NULL DEFAULT NULL,
                                       `void_stock_check_order_id` bigint(20) NULL DEFAULT NULL,
                                       `void_stock_in_order_id` bigint(20) NULL DEFAULT NULL,
                                       `void_stock_out_order_id` bigint(20) NULL DEFAULT NULL,
                                       `void_stock_transfer_order_id` bigint(20) NULL DEFAULT NULL,
                                       `warehouse_id` bigint(20) NOT NULL,
                                       PRIMARY KEY (`id`) USING BTREE,
                                       INDEX `flow_inventoryflow_creator_id_7ca2f31c_fk_system_user_id`(`creator_id` ASC) USING BTREE,
                                       INDEX `flow_inventoryflow_goods_id_5617d1cd_fk_goods_goods_id`(`goods_id` ASC) USING BTREE,
                                       INDEX `flow_inventoryflow_purchase_order_id_e3b47bfb_fk_purchase_`(`purchase_order_id` ASC) USING BTREE,
                                       INDEX `flow_inventoryflow_purchase_return_orde_2da1726f_fk_purchase_`(`purchase_return_order_id` ASC) USING BTREE,
                                       INDEX `flow_inventoryflow_sales_order_id_92ee3975_fk_sales_sal`(`sales_order_id` ASC) USING BTREE,
                                       INDEX `flow_inventoryflow_sales_return_order_i_8a2c7008_fk_sales_sal`(`sales_return_order_id` ASC) USING BTREE,
                                       INDEX `flow_inventoryflow_stock_check_order_id_a565e0fd_fk_stock_che`(`stock_check_order_id` ASC) USING BTREE,
                                       INDEX `flow_inventoryflow_stock_in_order_id_9082d777_fk_stock_in_`(`stock_in_order_id` ASC) USING BTREE,
                                       INDEX `flow_inventoryflow_stock_out_order_id_fa55260e_fk_stock_out`(`stock_out_order_id` ASC) USING BTREE,
                                       INDEX `flow_inventoryflow_stock_transfer_order_093ca5a6_fk_stock_tra`(`stock_transfer_order_id` ASC) USING BTREE,
                                       INDEX `flow_inventoryflow_team_id_6acb0689_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                       INDEX `flow_inventoryflow_void_purchase_order__779646b5_fk_purchase_`(`void_purchase_order_id` ASC) USING BTREE,
                                       INDEX `flow_inventoryflow_void_purchase_return_6bc2451a_fk_purchase_`(`void_purchase_return_order_id` ASC) USING BTREE,
                                       INDEX `flow_inventoryflow_void_sales_order_id_62baf5f5_fk_sales_sal`(`void_sales_order_id` ASC) USING BTREE,
                                       INDEX `flow_inventoryflow_void_sales_return_or_7c09f04a_fk_sales_sal`(`void_sales_return_order_id` ASC) USING BTREE,
                                       INDEX `flow_inventoryflow_void_stock_check_ord_8d94590e_fk_stock_che`(`void_stock_check_order_id` ASC) USING BTREE,
                                       INDEX `flow_inventoryflow_void_stock_in_order__92d035ad_fk_stock_in_`(`void_stock_in_order_id` ASC) USING BTREE,
                                       INDEX `flow_inventoryflow_void_stock_out_order_a88937b2_fk_stock_out`(`void_stock_out_order_id` ASC) USING BTREE,
                                       INDEX `flow_inventoryflow_void_stock_transfer__b2b54eae_fk_stock_tra`(`void_stock_transfer_order_id` ASC) USING BTREE,
                                       INDEX `flow_inventoryflow_warehouse_id_2582a93a_fk_data_warehouse_id`(`warehouse_id` ASC) USING BTREE,
                                       CONSTRAINT `flow_inventoryflow_creator_id_7ca2f31c_fk_system_user_id` FOREIGN KEY (`creator_id`) REFERENCES `system_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                       CONSTRAINT `flow_inventoryflow_goods_id_5617d1cd_fk_goods_goods_id` FOREIGN KEY (`goods_id`) REFERENCES `goods_goods` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                       CONSTRAINT `flow_inventoryflow_purchase_order_id_e3b47bfb_fk_purchase_` FOREIGN KEY (`purchase_order_id`) REFERENCES `purchase_purchaseorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                       CONSTRAINT `flow_inventoryflow_purchase_return_orde_2da1726f_fk_purchase_` FOREIGN KEY (`purchase_return_order_id`) REFERENCES `purchase_purchasereturnorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                       CONSTRAINT `flow_inventoryflow_sales_order_id_92ee3975_fk_sales_sal` FOREIGN KEY (`sales_order_id`) REFERENCES `sales_salesorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                       CONSTRAINT `flow_inventoryflow_sales_return_order_i_8a2c7008_fk_sales_sal` FOREIGN KEY (`sales_return_order_id`) REFERENCES `sales_salesreturnorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                       CONSTRAINT `flow_inventoryflow_stock_check_order_id_a565e0fd_fk_stock_che` FOREIGN KEY (`stock_check_order_id`) REFERENCES `stock_check_stockcheckorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                       CONSTRAINT `flow_inventoryflow_stock_in_order_id_9082d777_fk_stock_in_` FOREIGN KEY (`stock_in_order_id`) REFERENCES `stock_in_stockinorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                       CONSTRAINT `flow_inventoryflow_stock_out_order_id_fa55260e_fk_stock_out` FOREIGN KEY (`stock_out_order_id`) REFERENCES `stock_out_stockoutorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                       CONSTRAINT `flow_inventoryflow_stock_transfer_order_093ca5a6_fk_stock_tra` FOREIGN KEY (`stock_transfer_order_id`) REFERENCES `stock_transfer_stocktransferorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                       CONSTRAINT `flow_inventoryflow_team_id_6acb0689_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                       CONSTRAINT `flow_inventoryflow_void_purchase_order__779646b5_fk_purchase_` FOREIGN KEY (`void_purchase_order_id`) REFERENCES `purchase_purchaseorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                       CONSTRAINT `flow_inventoryflow_void_purchase_return_6bc2451a_fk_purchase_` FOREIGN KEY (`void_purchase_return_order_id`) REFERENCES `purchase_purchasereturnorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                       CONSTRAINT `flow_inventoryflow_void_sales_order_id_62baf5f5_fk_sales_sal` FOREIGN KEY (`void_sales_order_id`) REFERENCES `sales_salesorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                       CONSTRAINT `flow_inventoryflow_void_sales_return_or_7c09f04a_fk_sales_sal` FOREIGN KEY (`void_sales_return_order_id`) REFERENCES `sales_salesreturnorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                       CONSTRAINT `flow_inventoryflow_void_stock_check_ord_8d94590e_fk_stock_che` FOREIGN KEY (`void_stock_check_order_id`) REFERENCES `stock_check_stockcheckorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                       CONSTRAINT `flow_inventoryflow_void_stock_in_order__92d035ad_fk_stock_in_` FOREIGN KEY (`void_stock_in_order_id`) REFERENCES `stock_in_stockinorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                       CONSTRAINT `flow_inventoryflow_void_stock_out_order_a88937b2_fk_stock_out` FOREIGN KEY (`void_stock_out_order_id`) REFERENCES `stock_out_stockoutorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                       CONSTRAINT `flow_inventoryflow_void_stock_transfer__b2b54eae_fk_stock_tra` FOREIGN KEY (`void_stock_transfer_order_id`) REFERENCES `stock_transfer_stocktransferorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                       CONSTRAINT `flow_inventoryflow_warehouse_id_2582a93a_fk_data_warehouse_id` FOREIGN KEY (`warehouse_id`) REFERENCES `data_warehouse` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 32 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of flow_inventoryflow
-- ----------------------------
INSERT INTO `flow_inventoryflow` VALUES (21, 'stock_in', 0, 200, 200, '2024-05-17 07:07:16.238014', 6, 6, NULL, NULL, NULL, NULL, NULL, 10, NULL, NULL, 5, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 4);
INSERT INTO `flow_inventoryflow` VALUES (22, 'stock_in', 0, 100, 100, '2024-05-17 07:07:16.238124', 6, 7, NULL, NULL, NULL, NULL, NULL, 10, NULL, NULL, 5, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 4);
INSERT INTO `flow_inventoryflow` VALUES (23, 'stock_in', 200, 100, 300, '2024-05-17 07:07:53.287051', 6, 6, NULL, NULL, NULL, NULL, NULL, 10, NULL, NULL, 5, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 4);
INSERT INTO `flow_inventoryflow` VALUES (24, 'stock_in', 100, 100, 200, '2024-05-17 07:07:53.287224', 6, 7, NULL, NULL, NULL, NULL, NULL, 10, NULL, NULL, 5, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 4);
INSERT INTO `flow_inventoryflow` VALUES (25, 'stock_out', 300, 100, 200, '2024-05-17 07:09:17.667713', 6, 6, NULL, NULL, NULL, NULL, NULL, NULL, 9, NULL, 5, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 4);
INSERT INTO `flow_inventoryflow` VALUES (26, 'stock_check', 200, -100, 100, '2024-05-17 07:09:45.231920', 6, 6, NULL, NULL, NULL, NULL, 1, NULL, NULL, NULL, 5, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 4);
INSERT INTO `flow_inventoryflow` VALUES (27, 'stock_check', 200, -180, 20, '2024-05-20 10:40:18.896708', 6, 6, NULL, NULL, NULL, NULL, 2, NULL, NULL, NULL, 5, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 4);
INSERT INTO `flow_inventoryflow` VALUES (28, 'stock_check', 20, 180, 200, '2024-05-20 10:40:45.795274', 6, 6, NULL, NULL, NULL, NULL, 3, NULL, NULL, NULL, 5, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 4);
INSERT INTO `flow_inventoryflow` VALUES (29, 'stock_check', 200, 800, 1000, '2024-05-20 10:41:19.214381', 6, 7, NULL, NULL, NULL, NULL, 4, NULL, NULL, NULL, 5, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 4);
INSERT INTO `flow_inventoryflow` VALUES (30, 'stock_in', 200, 100, 300, '2024-07-06 18:23:28.696015', 6, 6, NULL, NULL, NULL, NULL, NULL, 12, NULL, NULL, 5, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 4);
INSERT INTO `flow_inventoryflow` VALUES (31, 'stock_in', 0, 1000, 1000, '2024-07-07 18:50:14.567319', 6, 8, NULL, NULL, NULL, NULL, NULL, 11, NULL, NULL, 5, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 4);

-- ----------------------------
-- Table structure for goods_batch
-- ----------------------------
DROP TABLE IF EXISTS `goods_batch`;
CREATE TABLE `goods_batch`  (
                                `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                `number` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                `initial_quantity` double NOT NULL,
                                `total_quantity` double NOT NULL,
                                `remain_quantity` double NOT NULL,
                                `production_date` date NULL DEFAULT NULL,
                                `shelf_life_days` int(11) NULL DEFAULT NULL,
                                `warning_date` date NULL DEFAULT NULL,
                                `expiration_date` date NULL DEFAULT NULL,
                                `has_stock` tinyint(1) NOT NULL,
                                `create_time` datetime(6) NOT NULL,
                                `goods_id` bigint(20) NOT NULL,
                                `inventory_id` bigint(20) NOT NULL,
                                `team_id` bigint(20) NOT NULL,
                                `warehouse_id` bigint(20) NOT NULL,
                                PRIMARY KEY (`id`) USING BTREE,
                                UNIQUE INDEX `goods_batch_number_warehouse_id_goods_id_team_id_9714a2b2_uniq`(`number` ASC, `warehouse_id` ASC, `goods_id` ASC, `team_id` ASC) USING BTREE,
                                INDEX `goods_batch_goods_id_f31251d8_fk_goods_goods_id`(`goods_id` ASC) USING BTREE,
                                INDEX `goods_batch_inventory_id_10b7ea6b_fk_goods_inventory_id`(`inventory_id` ASC) USING BTREE,
                                INDEX `goods_batch_team_id_f515c373_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                INDEX `goods_batch_warehouse_id_d4184472_fk_data_warehouse_id`(`warehouse_id` ASC) USING BTREE,
                                CONSTRAINT `goods_batch_goods_id_f31251d8_fk_goods_goods_id` FOREIGN KEY (`goods_id`) REFERENCES `goods_goods` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                CONSTRAINT `goods_batch_inventory_id_10b7ea6b_fk_goods_inventory_id` FOREIGN KEY (`inventory_id`) REFERENCES `goods_inventory` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                CONSTRAINT `goods_batch_team_id_f515c373_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                CONSTRAINT `goods_batch_warehouse_id_d4184472_fk_data_warehouse_id` FOREIGN KEY (`warehouse_id`) REFERENCES `data_warehouse` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of goods_batch
-- ----------------------------

-- ----------------------------
-- Table structure for goods_goods
-- ----------------------------
DROP TABLE IF EXISTS `goods_goods`;
CREATE TABLE `goods_goods`  (
                                `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                `number` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                `name` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                `barcode` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                `spec` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                `enable_batch_control` tinyint(1) NOT NULL,
                                `shelf_life_days` int(11) NULL DEFAULT NULL,
                                `shelf_life_warning_days` int(11) NOT NULL,
                                `enable_inventory_warning` tinyint(1) NOT NULL,
                                `inventory_upper` double NULL DEFAULT NULL,
                                `inventory_lower` double NULL DEFAULT NULL,
                                `purchase_price` double NOT NULL,
                                `retail_price` double NOT NULL,
                                `level_price1` double NOT NULL,
                                `level_price2` double NOT NULL,
                                `level_price3` double NOT NULL,
                                `remark` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                `is_active` tinyint(1) NOT NULL,
                                `category_id` bigint(20) NULL DEFAULT NULL,
                                `team_id` bigint(20) NOT NULL,
                                `unit_id` bigint(20) NULL DEFAULT NULL,
                                PRIMARY KEY (`id`) USING BTREE,
                                UNIQUE INDEX `goods_goods_number_team_id_ce62f88a_uniq`(`number` ASC, `team_id` ASC) USING BTREE,
                                INDEX `goods_goods_category_id_da3507dd_fk_goods_goodscategory_id`(`category_id` ASC) USING BTREE,
                                INDEX `goods_goods_team_id_c78d01c7_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                INDEX `goods_goods_unit_id_1dd5c544_fk_goods_goodsunit_id`(`unit_id` ASC) USING BTREE,
                                CONSTRAINT `goods_goods_category_id_da3507dd_fk_goods_goodscategory_id` FOREIGN KEY (`category_id`) REFERENCES `goods_goodscategory` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                CONSTRAINT `goods_goods_team_id_c78d01c7_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                CONSTRAINT `goods_goods_unit_id_1dd5c544_fk_goods_goodsunit_id` FOREIGN KEY (`unit_id`) REFERENCES `goods_goodsunit` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of goods_goods
-- ----------------------------
INSERT INTO `goods_goods` VALUES (6, 'G000000000001', '笔', NULL, NULL, 0, NULL, 0, 1, NULL, NULL, 0.5, 2, 0.8, 1.2, 1.5, NULL, 1, 9, 5, NULL);
INSERT INTO `goods_goods` VALUES (7, 'G000000000002', '削皮', NULL, NULL, 0, NULL, 0, 0, NULL, NULL, 0, 0, 0, 0, 0, NULL, 1, 9, 5, NULL);
INSERT INTO `goods_goods` VALUES (8, 'G000000000003', '1312', '3213213', '312', 0, 132, 0, 0, NULL, NULL, 0, 0, 0, 0, 0, NULL, 1, NULL, 5, NULL);
INSERT INTO `goods_goods` VALUES (9, 'G000000000004', '篮球', NULL, NULL, 0, NULL, 0, 0, NULL, NULL, 0, 0, 0, 0, 0, NULL, 1, NULL, 5, NULL);
INSERT INTO `goods_goods` VALUES (10, 'G000000000005', '积分', NULL, '规格', 0, 111, 0, 0, NULL, NULL, 0, 0.1, 0, 0, 0, '分', 1, 11, 5, NULL);
INSERT INTO `goods_goods` VALUES (11, 'G000000000006', '途牛积分', NULL, '账号：15392743940 密码：827632187', 0, NULL, 0, 0, NULL, NULL, 0, 0, 0, 0, 0, NULL, 1, NULL, 5, NULL);
INSERT INTO `goods_goods` VALUES (12, 'G000000000007', '途牛积分', NULL, NULL, 0, NULL, 0, 0, NULL, NULL, 0, 0, 0, 0, 0, NULL, 1, NULL, 5, NULL);
INSERT INTO `goods_goods` VALUES (13, 'G000000000008', '迪士尼成人票', NULL, NULL, 0, NULL, 0, 0, NULL, NULL, 0, 0, 0, 0, 0, NULL, 1, NULL, 5, NULL);
INSERT INTO `goods_goods` VALUES (14, 'G000000000009', '上海迪士尼儿童票', NULL, NULL, 0, NULL, 0, 0, NULL, NULL, 0, 0, 0, 0, 0, NULL, 1, NULL, 5, NULL);
INSERT INTO `goods_goods` VALUES (15, 'G000000000010', '红xiez', NULL, NULL, 0, NULL, 0, 0, NULL, NULL, 99, 0, 0, 0, 0, NULL, 1, 20, 5, NULL);
INSERT INTO `goods_goods` VALUES (16, 'G001', '产品A', NULL, NULL, 0, NULL, 0, 0, NULL, NULL, 10, 20, 20, 20, 20, NULL, 1, NULL, 3, NULL);

-- ----------------------------
-- Table structure for goods_goodscategory
-- ----------------------------
DROP TABLE IF EXISTS `goods_goodscategory`;
CREATE TABLE `goods_goodscategory`  (
                                        `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                        `name` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                        `remark` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                        `team_id` bigint(20) NOT NULL,
                                        `average_price` decimal(10, 2) NULL DEFAULT NULL,
                                        PRIMARY KEY (`id`) USING BTREE,
                                        UNIQUE INDEX `goods_goodscategory_name_team_id_ca476a3e_uniq`(`name` ASC, `team_id` ASC) USING BTREE,
                                        INDEX `goods_goodscategory_team_id_51b253d2_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                        CONSTRAINT `goods_goodscategory_team_id_51b253d2_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of goods_goodscategory
-- ----------------------------
INSERT INTO `goods_goodscategory` VALUES (9, '办公', NULL, 5, NULL);
INSERT INTO `goods_goodscategory` VALUES (11, '囧户籍科', 'kk', 5, NULL);
INSERT INTO `goods_goodscategory` VALUES (12, '宣教机', NULL, 5, NULL);
INSERT INTO `goods_goodscategory` VALUES (14, '饮料', NULL, 5, NULL);
INSERT INTO `goods_goodscategory` VALUES (17, '手表', '123', 5, NULL);
INSERT INTO `goods_goodscategory` VALUES (18, '次数', NULL, 5, NULL);
INSERT INTO `goods_goodscategory` VALUES (19, '金额', NULL, 5, NULL);
INSERT INTO `goods_goodscategory` VALUES (20, 'LL', NULL, 5, NULL);

-- ----------------------------
-- Table structure for goods_goodsimage
-- ----------------------------
DROP TABLE IF EXISTS `goods_goodsimage`;
CREATE TABLE `goods_goodsimage`  (
                                     `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                     `file` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                     `name` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                     `goods_id` bigint(20) NULL DEFAULT NULL,
                                     `team_id` bigint(20) NOT NULL,
                                     PRIMARY KEY (`id`) USING BTREE,
                                     INDEX `goods_goodsimage_goods_id_08cb23b1_fk_goods_goods_id`(`goods_id` ASC) USING BTREE,
                                     INDEX `goods_goodsimage_team_id_fcae4136_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                     CONSTRAINT `goods_goodsimage_goods_id_08cb23b1_fk_goods_goods_id` FOREIGN KEY (`goods_id`) REFERENCES `goods_goods` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                     CONSTRAINT `goods_goodsimage_team_id_fcae4136_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of goods_goodsimage
-- ----------------------------

-- ----------------------------
-- Table structure for goods_goodsunit
-- ----------------------------
DROP TABLE IF EXISTS `goods_goodsunit`;
CREATE TABLE `goods_goodsunit`  (
                                    `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                    `name` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                    `remark` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                    `team_id` bigint(20) NOT NULL,
                                    PRIMARY KEY (`id`) USING BTREE,
                                    UNIQUE INDEX `goods_goodsunit_name_team_id_b7d0ff14_uniq`(`name` ASC, `team_id` ASC) USING BTREE,
                                    INDEX `goods_goodsunit_team_id_11de59a6_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                    CONSTRAINT `goods_goodsunit_team_id_11de59a6_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of goods_goodsunit
-- ----------------------------
INSERT INTO `goods_goodsunit` VALUES (10, '分', '积分余额', 5);

-- ----------------------------
-- Table structure for goods_inventory
-- ----------------------------
DROP TABLE IF EXISTS `goods_inventory`;
CREATE TABLE `goods_inventory`  (
                                    `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                    `initial_quantity` double NOT NULL,
                                    `total_quantity` double NOT NULL,
                                    `has_stock` tinyint(1) NOT NULL,
                                    `goods_id` bigint(20) NOT NULL,
                                    `team_id` bigint(20) NOT NULL,
                                    `warehouse_id` bigint(20) NOT NULL,
                                    `predict_price` decimal(10, 2) NULL DEFAULT NULL,
                                    `predict_number` int(11) NULL DEFAULT NULL,
                                    PRIMARY KEY (`id`) USING BTREE,
                                    UNIQUE INDEX `goods_inventory_warehouse_id_goods_id_team_id_877c4770_uniq`(`warehouse_id` ASC, `goods_id` ASC, `team_id` ASC) USING BTREE,
                                    INDEX `goods_inventory_goods_id_315bae0f_fk_goods_goods_id`(`goods_id` ASC) USING BTREE,
                                    INDEX `goods_inventory_team_id_a1d30da1_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                    CONSTRAINT `goods_inventory_goods_id_315bae0f_fk_goods_goods_id` FOREIGN KEY (`goods_id`) REFERENCES `goods_goods` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                    CONSTRAINT `goods_inventory_team_id_a1d30da1_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                    CONSTRAINT `goods_inventory_warehouse_id_4cb4ab69_fk_data_warehouse_id` FOREIGN KEY (`warehouse_id`) REFERENCES `data_warehouse` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 34 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of goods_inventory
-- ----------------------------
INSERT INTO `goods_inventory` VALUES (10, 100, 300, 1, 6, 5, 4, NULL, NULL);
INSERT INTO `goods_inventory` VALUES (11, 0, 1000, 1, 7, 5, 4, NULL, NULL);
INSERT INTO `goods_inventory` VALUES (12, 0, 1000, 1, 8, 5, 4, NULL, NULL);
INSERT INTO `goods_inventory` VALUES (13, 0, 0, 0, 9, 5, 4, NULL, NULL);
INSERT INTO `goods_inventory` VALUES (18, 0, 0, 0, 6, 5, 6, NULL, NULL);
INSERT INTO `goods_inventory` VALUES (19, 0, 0, 0, 7, 5, 6, NULL, NULL);
INSERT INTO `goods_inventory` VALUES (20, 0, 0, 0, 8, 5, 6, NULL, NULL);
INSERT INTO `goods_inventory` VALUES (21, 0, 0, 0, 9, 5, 6, NULL, NULL);
INSERT INTO `goods_inventory` VALUES (22, 11, 11, 1, 10, 5, 4, NULL, NULL);
INSERT INTO `goods_inventory` VALUES (23, 0, 0, 0, 10, 5, 6, NULL, NULL);
INSERT INTO `goods_inventory` VALUES (24, 0, 0, 0, 11, 5, 4, NULL, NULL);
INSERT INTO `goods_inventory` VALUES (25, 0, 0, 0, 11, 5, 6, NULL, NULL);
INSERT INTO `goods_inventory` VALUES (26, 10000, 10000, 1, 12, 5, 4, NULL, NULL);
INSERT INTO `goods_inventory` VALUES (27, 0, 0, 0, 12, 5, 6, NULL, NULL);
INSERT INTO `goods_inventory` VALUES (28, 999, 999, 1, 13, 5, 4, NULL, NULL);
INSERT INTO `goods_inventory` VALUES (29, 0, 0, 0, 13, 5, 6, NULL, NULL);
INSERT INTO `goods_inventory` VALUES (30, 999, 999, 1, 14, 5, 4, NULL, NULL);
INSERT INTO `goods_inventory` VALUES (31, 0, 0, 0, 14, 5, 6, NULL, NULL);
INSERT INTO `goods_inventory` VALUES (32, 0, 0, 0, 15, 5, 4, NULL, NULL);
INSERT INTO `goods_inventory` VALUES (33, 0, 0, 0, 15, 5, 6, NULL, NULL);
INSERT INTO `goods_inventory` VALUES (34, 0, 0, 0, 16, 3, 7, NULL, NULL);

-- ----------------------------
-- Table structure for manage_device
-- ----------------------------
DROP TABLE IF EXISTS `manage_device`;
CREATE TABLE `manage_device`  (
                                  `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                  `number` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                  `name` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                  `model` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                  `serial_number` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                  `account_ownership` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of manage_device
-- ----------------------------

-- ----------------------------
-- Table structure for manage_superuser
-- ----------------------------
DROP TABLE IF EXISTS `manage_superuser`;
CREATE TABLE `manage_superuser`  (
                                     `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                     `password` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                     `last_login` datetime(6) NULL DEFAULT NULL,
                                     `username` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                     PRIMARY KEY (`id`) USING BTREE,
                                     UNIQUE INDEX `username`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of manage_superuser
-- ----------------------------

-- ----------------------------
-- Table structure for production_productionorder
-- ----------------------------
DROP TABLE IF EXISTS `production_productionorder`;
CREATE TABLE `production_productionorder`  (
                                               `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                               `number` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                               `is_related` tinyint(1) NOT NULL,
                                               `total_quantity` double NOT NULL,
                                               `quantity_produced` double NOT NULL,
                                               `remain_quantity` double NOT NULL,
                                               `start_time` datetime(6) NULL DEFAULT NULL,
                                               `end_time` datetime(6) NULL DEFAULT NULL,
                                               `status` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                               `create_time` datetime(6) NOT NULL,
                                               `creator_id` bigint(20) NOT NULL,
                                               `goods_id` bigint(20) NOT NULL,
                                               `sales_order_id` bigint(20) NULL DEFAULT NULL,
                                               `team_id` bigint(20) NOT NULL,
                                               PRIMARY KEY (`id`) USING BTREE,
                                               INDEX `production_productionorder_creator_id_5caa4d99_fk_system_user_id`(`creator_id` ASC) USING BTREE,
                                               INDEX `production_productionorder_goods_id_473152b7_fk_goods_goods_id`(`goods_id` ASC) USING BTREE,
                                               INDEX `production_productio_sales_order_id_580b6939_fk_sales_sal`(`sales_order_id` ASC) USING BTREE,
                                               INDEX `production_productionorder_team_id_2da946e4_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                               CONSTRAINT `production_productio_sales_order_id_580b6939_fk_sales_sal` FOREIGN KEY (`sales_order_id`) REFERENCES `sales_salesorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                               CONSTRAINT `production_productionorder_creator_id_5caa4d99_fk_system_user_id` FOREIGN KEY (`creator_id`) REFERENCES `system_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                               CONSTRAINT `production_productionorder_goods_id_473152b7_fk_goods_goods_id` FOREIGN KEY (`goods_id`) REFERENCES `goods_goods` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                               CONSTRAINT `production_productionorder_team_id_2da946e4_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of production_productionorder
-- ----------------------------

-- ----------------------------
-- Table structure for production_productionrecord
-- ----------------------------
DROP TABLE IF EXISTS `production_productionrecord`;
CREATE TABLE `production_productionrecord`  (
                                                `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                                `production_quantity` double NOT NULL,
                                                `create_time` datetime(6) NOT NULL,
                                                `creator_id` bigint(20) NOT NULL,
                                                `goods_id` bigint(20) NOT NULL,
                                                `production_order_id` bigint(20) NOT NULL,
                                                `team_id` bigint(20) NOT NULL,
                                                PRIMARY KEY (`id`) USING BTREE,
                                                INDEX `production_productio_creator_id_b48fb33f_fk_system_us`(`creator_id` ASC) USING BTREE,
                                                INDEX `production_productionrecord_goods_id_eb755106_fk_goods_goods_id`(`goods_id` ASC) USING BTREE,
                                                INDEX `production_productio_production_order_id_1fd5c4d6_fk_productio`(`production_order_id` ASC) USING BTREE,
                                                INDEX `production_productionrecord_team_id_48e4a119_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                                CONSTRAINT `production_productio_creator_id_b48fb33f_fk_system_us` FOREIGN KEY (`creator_id`) REFERENCES `system_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                CONSTRAINT `production_productio_production_order_id_1fd5c4d6_fk_productio` FOREIGN KEY (`production_order_id`) REFERENCES `production_productionorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                CONSTRAINT `production_productionrecord_goods_id_eb755106_fk_goods_goods_id` FOREIGN KEY (`goods_id`) REFERENCES `goods_goods` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                CONSTRAINT `production_productionrecord_team_id_48e4a119_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of production_productionrecord
-- ----------------------------

-- ----------------------------
-- Table structure for purchase_purchaseaccount
-- ----------------------------
DROP TABLE IF EXISTS `purchase_purchaseaccount`;
CREATE TABLE `purchase_purchaseaccount`  (
                                             `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                             `payment_amount` decimal(16, 2) NOT NULL,
                                             `account_id` bigint(20) NOT NULL,
                                             `purchase_order_id` bigint(20) NOT NULL,
                                             `team_id` bigint(20) NOT NULL,
                                             PRIMARY KEY (`id`) USING BTREE,
                                             UNIQUE INDEX `purchase_purchaseaccount_purchase_order_id_accoun_00bc7942_uniq`(`purchase_order_id` ASC, `account_id` ASC) USING BTREE,
                                             INDEX `purchase_purchaseaccount_account_id_8752c11f_fk_data_account_id`(`account_id` ASC) USING BTREE,
                                             INDEX `purchase_purchaseaccount_team_id_0fff95ed_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                             CONSTRAINT `purchase_purchaseacc_purchase_order_id_c71f288a_fk_purchase_` FOREIGN KEY (`purchase_order_id`) REFERENCES `purchase_purchaseorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                             CONSTRAINT `purchase_purchaseaccount_account_id_8752c11f_fk_data_account_id` FOREIGN KEY (`account_id`) REFERENCES `data_account` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                             CONSTRAINT `purchase_purchaseaccount_team_id_0fff95ed_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of purchase_purchaseaccount
-- ----------------------------

-- ----------------------------
-- Table structure for purchase_purchasegoods
-- ----------------------------
DROP TABLE IF EXISTS `purchase_purchasegoods`;
CREATE TABLE `purchase_purchasegoods`  (
                                           `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                           `purchase_quantity` double NOT NULL,
                                           `purchase_price` double NOT NULL,
                                           `total_amount` decimal(16, 2) NOT NULL,
                                           `return_quantity` double NOT NULL,
                                           `goods_id` bigint(20) NOT NULL,
                                           `purchase_order_id` bigint(20) NOT NULL,
                                           `team_id` bigint(20) NOT NULL,
                                           PRIMARY KEY (`id`) USING BTREE,
                                           UNIQUE INDEX `purchase_purchasegoods_purchase_order_id_goods_id_b3ca2aad_uniq`(`purchase_order_id` ASC, `goods_id` ASC) USING BTREE,
                                           INDEX `purchase_purchasegoods_goods_id_9575a6ac_fk_goods_goods_id`(`goods_id` ASC) USING BTREE,
                                           INDEX `purchase_purchasegoods_team_id_65acf0bd_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                           CONSTRAINT `purchase_purchasegoo_purchase_order_id_13ca1d79_fk_purchase_` FOREIGN KEY (`purchase_order_id`) REFERENCES `purchase_purchaseorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                           CONSTRAINT `purchase_purchasegoods_goods_id_9575a6ac_fk_goods_goods_id` FOREIGN KEY (`goods_id`) REFERENCES `goods_goods` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                           CONSTRAINT `purchase_purchasegoods_team_id_65acf0bd_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 31 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of purchase_purchasegoods
-- ----------------------------
INSERT INTO `purchase_purchasegoods` VALUES (15, 200, 15.450000000000001, 3090.00, 0, 7, 15, 5);
INSERT INTO `purchase_purchasegoods` VALUES (16, 300, 15.450000000000001, 4635.00, 0, 6, 15, 5);
INSERT INTO `purchase_purchasegoods` VALUES (17, 1000, 101, 101000.00, 1000, 8, 16, 5);
INSERT INTO `purchase_purchasegoods` VALUES (26, 300, 110.00000000000001, 33000.00, 0, 9, 21, 5);
INSERT INTO `purchase_purchasegoods` VALUES (27, 50, 50.5, 2525.00, 0, 9, 22, 5);
INSERT INTO `purchase_purchasegoods` VALUES (28, 3000, 0.97, 2910.00, 0, 10, 23, 5);
INSERT INTO `purchase_purchasegoods` VALUES (29, 100, 99, 9900.00, 0, 15, 24, 5);
INSERT INTO `purchase_purchasegoods` VALUES (30, 50, 50.5, 2525.00, 0, 13, 25, 5);

-- ----------------------------
-- Table structure for purchase_purchaseorder
-- ----------------------------
DROP TABLE IF EXISTS `purchase_purchaseorder`;
CREATE TABLE `purchase_purchaseorder`  (
                                           `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                           `number` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                           `handle_time` date NOT NULL,
                                           `remark` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                           `total_quantity` double NULL DEFAULT NULL,
                                           `other_amount` decimal(16, 2) NOT NULL,
                                           `total_amount` decimal(16, 2) NULL DEFAULT NULL,
                                           `payment_amount` decimal(16, 2) NULL DEFAULT NULL,
                                           `arrears_amount` decimal(16, 2) NULL DEFAULT NULL,
                                           `is_void` tinyint(1) NOT NULL,
                                           `enable_auto_stock_in` tinyint(1) NOT NULL,
                                           `create_time` datetime(6) NOT NULL,
                                           `creator_id` bigint(20) NOT NULL,
                                           `handler_id` bigint(20) NOT NULL,
                                           `supplier_id` bigint(20) NOT NULL,
                                           `team_id` bigint(20) NOT NULL,
                                           `warehouse_id` bigint(20) NOT NULL,
                                           PRIMARY KEY (`id`) USING BTREE,
                                           UNIQUE INDEX `purchase_purchaseorder_number_team_id_38087ff8_uniq`(`number` ASC, `team_id` ASC) USING BTREE,
                                           INDEX `purchase_purchaseorder_creator_id_948c80b6_fk_system_user_id`(`creator_id` ASC) USING BTREE,
                                           INDEX `purchase_purchaseorder_handler_id_73b778e1_fk_system_user_id`(`handler_id` ASC) USING BTREE,
                                           INDEX `purchase_purchaseorder_supplier_id_2afd9c3c_fk_data_supplier_id`(`supplier_id` ASC) USING BTREE,
                                           INDEX `purchase_purchaseorder_team_id_fa5ea74b_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                           INDEX `purchase_purchaseord_warehouse_id_a3b24fc7_fk_data_ware`(`warehouse_id` ASC) USING BTREE,
                                           CONSTRAINT `purchase_purchaseord_warehouse_id_a3b24fc7_fk_data_ware` FOREIGN KEY (`warehouse_id`) REFERENCES `data_warehouse` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                           CONSTRAINT `purchase_purchaseorder_creator_id_948c80b6_fk_system_user_id` FOREIGN KEY (`creator_id`) REFERENCES `system_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                           CONSTRAINT `purchase_purchaseorder_handler_id_73b778e1_fk_system_user_id` FOREIGN KEY (`handler_id`) REFERENCES `system_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                           CONSTRAINT `purchase_purchaseorder_supplier_id_2afd9c3c_fk_data_supplier_id` FOREIGN KEY (`supplier_id`) REFERENCES `data_supplier` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                           CONSTRAINT `purchase_purchaseorder_team_id_fa5ea74b_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 26 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of purchase_purchaseorder
-- ----------------------------
INSERT INTO `purchase_purchaseorder` VALUES (15, 'CG202405170001', '2024-05-17', NULL, 500, 0.00, 7725.00, 0.00, 7725.00, 0, 0, '2024-05-17 07:06:13.043742', 6, 6, 4, 5, 4);
INSERT INTO `purchase_purchaseorder` VALUES (16, 'CG202406280001', '2024-06-07', NULL, 1000, 0.00, 101000.00, 0.00, 101000.00, 0, 0, '2024-06-28 14:40:19.350579', 6, 8, 4, 5, 4);
INSERT INTO `purchase_purchaseorder` VALUES (21, 'CG202407090001', '2024-07-09', '测试', 300, 0.00, 33000.00, 0.00, 33000.00, 0, 0, '2024-07-09 02:38:11.783667', 6, 7, 5, 5, 4);
INSERT INTO `purchase_purchaseorder` VALUES (22, 'CG202407100001', '2024-07-10', NULL, 50, 0.00, 2525.00, 0.00, 2525.00, 0, 0, '2024-07-10 03:59:00.824230', 6, 6, 4, 5, 6);
INSERT INTO `purchase_purchaseorder` VALUES (23, 'CG202407120001', '2024-07-12', NULL, 3000, 0.00, 2910.00, 0.00, 2910.00, 0, 0, '2024-07-12 13:38:25.062967', 6, 7, 4, 5, 6);
INSERT INTO `purchase_purchaseorder` VALUES (24, 'CG202407190001', '2024-07-19', NULL, 100, 0.00, 9900.00, 0.00, 9900.00, 0, 0, '2024-07-19 07:16:05.442695', 6, 6, 7, 5, 4);
INSERT INTO `purchase_purchaseorder` VALUES (25, 'CG202407260001', '2024-07-26', NULL, 50, 50.00, 2575.00, 0.00, 2575.00, 0, 0, '2024-07-25 16:43:56.014218', 6, 8, 4, 5, 4);

-- ----------------------------
-- Table structure for purchase_purchasereturnaccount
-- ----------------------------
DROP TABLE IF EXISTS `purchase_purchasereturnaccount`;
CREATE TABLE `purchase_purchasereturnaccount`  (
                                                   `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                                   `collection_amount` decimal(16, 2) NOT NULL,
                                                   `account_id` bigint(20) NOT NULL,
                                                   `purchase_return_order_id` bigint(20) NOT NULL,
                                                   `team_id` bigint(20) NOT NULL,
                                                   PRIMARY KEY (`id`) USING BTREE,
                                                   UNIQUE INDEX `purchase_purchasereturna_purchase_return_order_id_3c6fb37d_uniq`(`purchase_return_order_id` ASC, `account_id` ASC) USING BTREE,
                                                   INDEX `purchase_purchaseret_account_id_2e400520_fk_data_acco`(`account_id` ASC) USING BTREE,
                                                   INDEX `purchase_purchaseret_team_id_ae678d9e_fk_system_te`(`team_id` ASC) USING BTREE,
                                                   CONSTRAINT `purchase_purchaseret_account_id_2e400520_fk_data_acco` FOREIGN KEY (`account_id`) REFERENCES `data_account` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                   CONSTRAINT `purchase_purchaseret_purchase_return_orde_a4b1c42b_fk_purchase_` FOREIGN KEY (`purchase_return_order_id`) REFERENCES `purchase_purchasereturnorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                   CONSTRAINT `purchase_purchaseret_team_id_ae678d9e_fk_system_te` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of purchase_purchasereturnaccount
-- ----------------------------

-- ----------------------------
-- Table structure for purchase_purchasereturngoods
-- ----------------------------
DROP TABLE IF EXISTS `purchase_purchasereturngoods`;
CREATE TABLE `purchase_purchasereturngoods`  (
                                                 `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                                 `return_quantity` double NOT NULL,
                                                 `return_price` double NOT NULL,
                                                 `total_amount` decimal(16, 2) NOT NULL,
                                                 `goods_id` bigint(20) NOT NULL,
                                                 `purchase_goods_id` bigint(20) NULL DEFAULT NULL,
                                                 `purchase_return_order_id` bigint(20) NOT NULL,
                                                 `team_id` bigint(20) NOT NULL,
                                                 PRIMARY KEY (`id`) USING BTREE,
                                                 UNIQUE INDEX `purchase_purchasereturng_purchase_return_order_id_8b000de5_uniq`(`purchase_return_order_id` ASC, `goods_id` ASC) USING BTREE,
                                                 INDEX `purchase_purchasereturngoods_goods_id_c57eb5cb_fk_goods_goods_id`(`goods_id` ASC) USING BTREE,
                                                 INDEX `purchase_purchaseret_purchase_goods_id_b0d99f91_fk_purchase_`(`purchase_goods_id` ASC) USING BTREE,
                                                 INDEX `purchase_purchasereturngoods_team_id_57e60ddc_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                                 CONSTRAINT `purchase_purchaseret_purchase_goods_id_b0d99f91_fk_purchase_` FOREIGN KEY (`purchase_goods_id`) REFERENCES `purchase_purchasegoods` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                 CONSTRAINT `purchase_purchaseret_purchase_return_orde_4f1a140a_fk_purchase_` FOREIGN KEY (`purchase_return_order_id`) REFERENCES `purchase_purchasereturnorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                 CONSTRAINT `purchase_purchasereturngoods_goods_id_c57eb5cb_fk_goods_goods_id` FOREIGN KEY (`goods_id`) REFERENCES `goods_goods` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                 CONSTRAINT `purchase_purchasereturngoods_team_id_57e60ddc_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of purchase_purchasereturngoods
-- ----------------------------
INSERT INTO `purchase_purchasereturngoods` VALUES (2, 1000, 101, 101000.00, 8, 17, 2, 5);

-- ----------------------------
-- Table structure for purchase_purchasereturnorder
-- ----------------------------
DROP TABLE IF EXISTS `purchase_purchasereturnorder`;
CREATE TABLE `purchase_purchasereturnorder`  (
                                                 `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                                 `number` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                                 `handle_time` date NOT NULL,
                                                 `remark` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                                 `total_quantity` double NULL DEFAULT NULL,
                                                 `other_amount` decimal(16, 2) NOT NULL,
                                                 `total_amount` decimal(16, 2) NULL DEFAULT NULL,
                                                 `collection_amount` decimal(16, 2) NULL DEFAULT NULL,
                                                 `arrears_amount` decimal(16, 2) NULL DEFAULT NULL,
                                                 `is_void` tinyint(1) NOT NULL,
                                                 `enable_auto_stock_out` tinyint(1) NOT NULL,
                                                 `create_time` datetime(6) NOT NULL,
                                                 `creator_id` bigint(20) NOT NULL,
                                                 `handler_id` bigint(20) NOT NULL,
                                                 `purchase_order_id` bigint(20) NULL DEFAULT NULL,
                                                 `supplier_id` bigint(20) NOT NULL,
                                                 `team_id` bigint(20) NOT NULL,
                                                 `warehouse_id` bigint(20) NOT NULL,
                                                 PRIMARY KEY (`id`) USING BTREE,
                                                 UNIQUE INDEX `purchase_purchasereturnorder_number_team_id_b1d415e2_uniq`(`number` ASC, `team_id` ASC) USING BTREE,
                                                 INDEX `purchase_purchaseret_creator_id_ffca4579_fk_system_us`(`creator_id` ASC) USING BTREE,
                                                 INDEX `purchase_purchaseret_handler_id_cb050686_fk_system_us`(`handler_id` ASC) USING BTREE,
                                                 INDEX `purchase_purchaseret_purchase_order_id_d645ebc2_fk_purchase_`(`purchase_order_id` ASC) USING BTREE,
                                                 INDEX `purchase_purchaseret_supplier_id_53b15f57_fk_data_supp`(`supplier_id` ASC) USING BTREE,
                                                 INDEX `purchase_purchasereturnorder_team_id_cf80e324_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                                 INDEX `purchase_purchaseret_warehouse_id_4946b151_fk_data_ware`(`warehouse_id` ASC) USING BTREE,
                                                 CONSTRAINT `purchase_purchaseret_creator_id_ffca4579_fk_system_us` FOREIGN KEY (`creator_id`) REFERENCES `system_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                 CONSTRAINT `purchase_purchaseret_handler_id_cb050686_fk_system_us` FOREIGN KEY (`handler_id`) REFERENCES `system_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                 CONSTRAINT `purchase_purchaseret_purchase_order_id_d645ebc2_fk_purchase_` FOREIGN KEY (`purchase_order_id`) REFERENCES `purchase_purchaseorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                 CONSTRAINT `purchase_purchaseret_supplier_id_53b15f57_fk_data_supp` FOREIGN KEY (`supplier_id`) REFERENCES `data_supplier` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                 CONSTRAINT `purchase_purchaseret_warehouse_id_4946b151_fk_data_ware` FOREIGN KEY (`warehouse_id`) REFERENCES `data_warehouse` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                 CONSTRAINT `purchase_purchasereturnorder_team_id_cf80e324_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of purchase_purchasereturnorder
-- ----------------------------
INSERT INTO `purchase_purchasereturnorder` VALUES (2, 'CR202406300001', '2024-06-15', NULL, 1000, 0.00, 101000.00, 0.00, 101000.00, 0, 0, '2024-06-30 14:14:24.996664', 6, 8, 16, 4, 5, 4);

-- ----------------------------
-- Table structure for sales_salesaccount
-- ----------------------------
DROP TABLE IF EXISTS `sales_salesaccount`;
CREATE TABLE `sales_salesaccount`  (
                                       `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                       `collection_amount` decimal(16, 2) NOT NULL,
                                       `account_id` bigint(20) NOT NULL,
                                       `sales_order_id` bigint(20) NOT NULL,
                                       `team_id` bigint(20) NOT NULL,
                                       PRIMARY KEY (`id`) USING BTREE,
                                       UNIQUE INDEX `sales_salesaccount_sales_order_id_account_id_0c99a441_uniq`(`sales_order_id` ASC, `account_id` ASC) USING BTREE,
                                       INDEX `sales_salesaccount_account_id_362f2f5a_fk_data_account_id`(`account_id` ASC) USING BTREE,
                                       INDEX `sales_salesaccount_team_id_9dee66b7_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                       CONSTRAINT `sales_salesaccount_account_id_362f2f5a_fk_data_account_id` FOREIGN KEY (`account_id`) REFERENCES `data_account` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                       CONSTRAINT `sales_salesaccount_sales_order_id_dabd3c19_fk_sales_sal` FOREIGN KEY (`sales_order_id`) REFERENCES `sales_salesorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                       CONSTRAINT `sales_salesaccount_team_id_9dee66b7_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of sales_salesaccount
-- ----------------------------

-- ----------------------------
-- Table structure for sales_salesgoods
-- ----------------------------
DROP TABLE IF EXISTS `sales_salesgoods`;
CREATE TABLE `sales_salesgoods`  (
                                     `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                     `sales_quantity` double NOT NULL,
                                     `sales_price` double NOT NULL,
                                     `total_amount` decimal(16, 2) NOT NULL,
                                     `return_quantity` double NOT NULL,
                                     `goods_id` bigint(20) NOT NULL,
                                     `sales_order_id` bigint(20) NOT NULL,
                                     `team_id` bigint(20) NOT NULL,
                                     PRIMARY KEY (`id`) USING BTREE,
                                     UNIQUE INDEX `sales_salesgoods_sales_order_id_goods_id_0c65b93a_uniq`(`sales_order_id` ASC, `goods_id` ASC) USING BTREE,
                                     INDEX `sales_salesgoods_goods_id_89b92ac7_fk_goods_goods_id`(`goods_id` ASC) USING BTREE,
                                     INDEX `sales_salesgoods_team_id_ce174403_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                     CONSTRAINT `sales_salesgoods_goods_id_89b92ac7_fk_goods_goods_id` FOREIGN KEY (`goods_id`) REFERENCES `goods_goods` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                     CONSTRAINT `sales_salesgoods_sales_order_id_399db0d3_fk_sales_salesorder_id` FOREIGN KEY (`sales_order_id`) REFERENCES `sales_salesorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                     CONSTRAINT `sales_salesgoods_team_id_ce174403_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 19 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of sales_salesgoods
-- ----------------------------
INSERT INTO `sales_salesgoods` VALUES (14, 100, 1, 100.00, 100, 6, 14, 5);
INSERT INTO `sales_salesgoods` VALUES (15, 1, 7.07, 7.07, 0, 8, 15, 5);
INSERT INTO `sales_salesgoods` VALUES (16, 333, 11.11, 3699.63, 0, 7, 16, 5);
INSERT INTO `sales_salesgoods` VALUES (17, 222, 22.22, 4932.84, 0, 6, 16, 5);
INSERT INTO `sales_salesgoods` VALUES (18, 1, 1.01, 1.01, 0, 7, 17, 5);

-- ----------------------------
-- Table structure for sales_salesorder
-- ----------------------------
DROP TABLE IF EXISTS `sales_salesorder`;
CREATE TABLE `sales_salesorder`  (
                                     `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                     `number` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                     `handle_time` date NOT NULL,
                                     `remark` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                     `total_quantity` double NULL DEFAULT NULL,
                                     `discount` double NOT NULL,
                                     `other_amount` decimal(16, 2) NOT NULL,
                                     `total_amount` decimal(16, 2) NULL DEFAULT NULL,
                                     `collection_amount` decimal(16, 2) NULL DEFAULT NULL,
                                     `arrears_amount` decimal(16, 2) NULL DEFAULT NULL,
                                     `is_void` tinyint(1) NOT NULL,
                                     `enable_auto_stock_out` tinyint(1) NOT NULL,
                                     `create_time` datetime(6) NOT NULL,
                                     `client_id` bigint(20) NOT NULL,
                                     `creator_id` bigint(20) NOT NULL,
                                     `handler_id` bigint(20) NOT NULL,
                                     `team_id` bigint(20) NOT NULL,
                                     `warehouse_id` bigint(20) NOT NULL,
                                     PRIMARY KEY (`id`) USING BTREE,
                                     UNIQUE INDEX `sales_salesorder_number_team_id_36ee9523_uniq`(`number` ASC, `team_id` ASC) USING BTREE,
                                     INDEX `sales_salesorder_client_id_e7fbd2f3_fk_data_client_id`(`client_id` ASC) USING BTREE,
                                     INDEX `sales_salesorder_creator_id_33fbe415_fk_system_user_id`(`creator_id` ASC) USING BTREE,
                                     INDEX `sales_salesorder_handler_id_b8a147dc_fk_system_user_id`(`handler_id` ASC) USING BTREE,
                                     INDEX `sales_salesorder_team_id_84be6810_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                     INDEX `sales_salesorder_warehouse_id_b03f5f4c_fk_data_warehouse_id`(`warehouse_id` ASC) USING BTREE,
                                     CONSTRAINT `sales_salesorder_client_id_e7fbd2f3_fk_data_client_id` FOREIGN KEY (`client_id`) REFERENCES `data_client` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                     CONSTRAINT `sales_salesorder_creator_id_33fbe415_fk_system_user_id` FOREIGN KEY (`creator_id`) REFERENCES `system_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                     CONSTRAINT `sales_salesorder_handler_id_b8a147dc_fk_system_user_id` FOREIGN KEY (`handler_id`) REFERENCES `system_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                     CONSTRAINT `sales_salesorder_team_id_84be6810_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                     CONSTRAINT `sales_salesorder_warehouse_id_b03f5f4c_fk_data_warehouse_id` FOREIGN KEY (`warehouse_id`) REFERENCES `data_warehouse` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 18 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of sales_salesorder
-- ----------------------------
INSERT INTO `sales_salesorder` VALUES (14, 'XS202405170001', '2024-05-17', NULL, 100, 100, 0.00, 100.00, 0.00, 100.00, 0, 0, '2024-05-17 07:08:53.407578', 4, 6, 6, 5, 4);
INSERT INTO `sales_salesorder` VALUES (15, 'XS202406300001', '2024-06-22', NULL, 1, 100, 0.00, 7.07, 0.00, 7.07, 1, 0, '2024-06-30 14:30:55.119797', 8, 6, 6, 5, 4);
INSERT INTO `sales_salesorder` VALUES (16, 'XS202407070001', '2024-07-07', NULL, 555, 100, 0.00, 8632.47, 0.00, 8632.47, 0, 0, '2024-07-06 18:30:47.547071', 4, 6, 8, 5, 4);
INSERT INTO `sales_salesorder` VALUES (17, 'XS202407290001', '2024-07-31', NULL, 1, 100, 0.00, 1.01, 0.00, 1.01, 0, 0, '2024-07-29 06:57:08.282141', 5, 6, 8, 5, 4);

-- ----------------------------
-- Table structure for sales_salesreturnaccount
-- ----------------------------
DROP TABLE IF EXISTS `sales_salesreturnaccount`;
CREATE TABLE `sales_salesreturnaccount`  (
                                             `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                             `payment_amount` decimal(16, 2) NOT NULL,
                                             `account_id` bigint(20) NOT NULL,
                                             `sales_return_order_id` bigint(20) NOT NULL,
                                             `team_id` bigint(20) NOT NULL,
                                             PRIMARY KEY (`id`) USING BTREE,
                                             UNIQUE INDEX `sales_salesreturnaccount_sales_return_order_id_ac_53487852_uniq`(`sales_return_order_id` ASC, `account_id` ASC) USING BTREE,
                                             INDEX `sales_salesreturnaccount_account_id_3ebe0d0e_fk_data_account_id`(`account_id` ASC) USING BTREE,
                                             INDEX `sales_salesreturnaccount_team_id_297748b1_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                             CONSTRAINT `sales_salesreturnacc_sales_return_order_i_5be33acb_fk_sales_sal` FOREIGN KEY (`sales_return_order_id`) REFERENCES `sales_salesreturnorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                             CONSTRAINT `sales_salesreturnaccount_account_id_3ebe0d0e_fk_data_account_id` FOREIGN KEY (`account_id`) REFERENCES `data_account` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                             CONSTRAINT `sales_salesreturnaccount_team_id_297748b1_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of sales_salesreturnaccount
-- ----------------------------

-- ----------------------------
-- Table structure for sales_salesreturngoods
-- ----------------------------
DROP TABLE IF EXISTS `sales_salesreturngoods`;
CREATE TABLE `sales_salesreturngoods`  (
                                           `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                           `return_quantity` double NOT NULL,
                                           `return_price` double NOT NULL,
                                           `total_amount` decimal(16, 2) NOT NULL,
                                           `goods_id` bigint(20) NOT NULL,
                                           `sales_goods_id` bigint(20) NULL DEFAULT NULL,
                                           `sales_return_order_id` bigint(20) NOT NULL,
                                           `team_id` bigint(20) NOT NULL,
                                           PRIMARY KEY (`id`) USING BTREE,
                                           UNIQUE INDEX `sales_salesreturngoods_sales_return_order_id_go_49267698_uniq`(`sales_return_order_id` ASC, `goods_id` ASC) USING BTREE,
                                           INDEX `sales_salesreturngoods_goods_id_57ee63b3_fk_goods_goods_id`(`goods_id` ASC) USING BTREE,
                                           INDEX `sales_salesreturngoo_sales_goods_id_ba81d419_fk_sales_sal`(`sales_goods_id` ASC) USING BTREE,
                                           INDEX `sales_salesreturngoods_team_id_cae113d4_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                           CONSTRAINT `sales_salesreturngoo_sales_goods_id_ba81d419_fk_sales_sal` FOREIGN KEY (`sales_goods_id`) REFERENCES `sales_salesgoods` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                           CONSTRAINT `sales_salesreturngoo_sales_return_order_i_ff120e37_fk_sales_sal` FOREIGN KEY (`sales_return_order_id`) REFERENCES `sales_salesreturnorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                           CONSTRAINT `sales_salesreturngoods_goods_id_57ee63b3_fk_goods_goods_id` FOREIGN KEY (`goods_id`) REFERENCES `goods_goods` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                           CONSTRAINT `sales_salesreturngoods_team_id_cae113d4_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of sales_salesreturngoods
-- ----------------------------
INSERT INTO `sales_salesreturngoods` VALUES (3, 100, 1, 100.00, 6, 14, 3, 5);

-- ----------------------------
-- Table structure for sales_salesreturnorder
-- ----------------------------
DROP TABLE IF EXISTS `sales_salesreturnorder`;
CREATE TABLE `sales_salesreturnorder`  (
                                           `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                           `number` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                           `handle_time` date NOT NULL,
                                           `remark` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                           `total_quantity` double NULL DEFAULT NULL,
                                           `other_amount` decimal(16, 2) NOT NULL,
                                           `total_amount` decimal(16, 2) NULL DEFAULT NULL,
                                           `payment_amount` decimal(16, 2) NULL DEFAULT NULL,
                                           `arrears_amount` decimal(16, 2) NULL DEFAULT NULL,
                                           `is_void` tinyint(1) NOT NULL,
                                           `enable_auto_stock_in` tinyint(1) NOT NULL,
                                           `create_time` datetime(6) NOT NULL,
                                           `client_id` bigint(20) NOT NULL,
                                           `creator_id` bigint(20) NOT NULL,
                                           `handler_id` bigint(20) NOT NULL,
                                           `sales_order_id` bigint(20) NULL DEFAULT NULL,
                                           `team_id` bigint(20) NOT NULL,
                                           `warehouse_id` bigint(20) NOT NULL,
                                           PRIMARY KEY (`id`) USING BTREE,
                                           UNIQUE INDEX `sales_salesreturnorder_number_team_id_7bfeea17_uniq`(`number` ASC, `team_id` ASC) USING BTREE,
                                           INDEX `sales_salesreturnorder_client_id_7a85e322_fk_data_client_id`(`client_id` ASC) USING BTREE,
                                           INDEX `sales_salesreturnorder_creator_id_ba15a0cc_fk_system_user_id`(`creator_id` ASC) USING BTREE,
                                           INDEX `sales_salesreturnorder_handler_id_dfca34ff_fk_system_user_id`(`handler_id` ASC) USING BTREE,
                                           INDEX `sales_salesreturnord_sales_order_id_f128ba7f_fk_sales_sal`(`sales_order_id` ASC) USING BTREE,
                                           INDEX `sales_salesreturnorder_team_id_14512882_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                           INDEX `sales_salesreturnord_warehouse_id_7e5690b7_fk_data_ware`(`warehouse_id` ASC) USING BTREE,
                                           CONSTRAINT `sales_salesreturnord_sales_order_id_f128ba7f_fk_sales_sal` FOREIGN KEY (`sales_order_id`) REFERENCES `sales_salesorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                           CONSTRAINT `sales_salesreturnord_warehouse_id_7e5690b7_fk_data_ware` FOREIGN KEY (`warehouse_id`) REFERENCES `data_warehouse` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                           CONSTRAINT `sales_salesreturnorder_client_id_7a85e322_fk_data_client_id` FOREIGN KEY (`client_id`) REFERENCES `data_client` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                           CONSTRAINT `sales_salesreturnorder_creator_id_ba15a0cc_fk_system_user_id` FOREIGN KEY (`creator_id`) REFERENCES `system_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                           CONSTRAINT `sales_salesreturnorder_handler_id_dfca34ff_fk_system_user_id` FOREIGN KEY (`handler_id`) REFERENCES `system_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                           CONSTRAINT `sales_salesreturnorder_team_id_14512882_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of sales_salesreturnorder
-- ----------------------------
INSERT INTO `sales_salesreturnorder` VALUES (3, 'SR202406300001', '2024-06-14', NULL, 100, 0.00, 100.00, 0.00, 100.00, 0, 0, '2024-06-30 14:40:47.211992', 4, 6, 6, 14, 5, 4);

-- ----------------------------
-- Table structure for stock_check_stockcheckbatch
-- ----------------------------
DROP TABLE IF EXISTS `stock_check_stockcheckbatch`;
CREATE TABLE `stock_check_stockcheckbatch`  (
                                                `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                                `batch_number` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                                `production_date` date NULL DEFAULT NULL,
                                                `book_quantity` double NOT NULL,
                                                `actual_quantity` double NOT NULL,
                                                `surplus_quantity` double NOT NULL,
                                                `status` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                                `goods_id` bigint(20) NOT NULL,
                                                `stock_check_goods_id` bigint(20) NOT NULL,
                                                `stock_check_order_id` bigint(20) NOT NULL,
                                                `team_id` bigint(20) NOT NULL,
                                                PRIMARY KEY (`id`) USING BTREE,
                                                UNIQUE INDEX `stock_check_stockcheckba_stock_check_goods_id_bat_a7fcf372_uniq`(`stock_check_goods_id` ASC, `batch_number` ASC) USING BTREE,
                                                INDEX `stock_check_stockcheckbatch_goods_id_137f6d92_fk_goods_goods_id`(`goods_id` ASC) USING BTREE,
                                                INDEX `stock_check_stockche_stock_check_order_id_7f313575_fk_stock_che`(`stock_check_order_id` ASC) USING BTREE,
                                                INDEX `stock_check_stockcheckbatch_team_id_f457c2a8_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                                CONSTRAINT `stock_check_stockche_stock_check_goods_id_07b68554_fk_stock_che` FOREIGN KEY (`stock_check_goods_id`) REFERENCES `stock_check_stockcheckgoods` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                CONSTRAINT `stock_check_stockche_stock_check_order_id_7f313575_fk_stock_che` FOREIGN KEY (`stock_check_order_id`) REFERENCES `stock_check_stockcheckorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                CONSTRAINT `stock_check_stockcheckbatch_goods_id_137f6d92_fk_goods_goods_id` FOREIGN KEY (`goods_id`) REFERENCES `goods_goods` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                CONSTRAINT `stock_check_stockcheckbatch_team_id_f457c2a8_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of stock_check_stockcheckbatch
-- ----------------------------

-- ----------------------------
-- Table structure for stock_check_stockcheckgoods
-- ----------------------------
DROP TABLE IF EXISTS `stock_check_stockcheckgoods`;
CREATE TABLE `stock_check_stockcheckgoods`  (
                                                `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                                `book_quantity` double NOT NULL,
                                                `actual_quantity` double NOT NULL,
                                                `surplus_quantity` double NOT NULL,
                                                `purchase_price` double NOT NULL,
                                                `surplus_amount` decimal(16, 2) NOT NULL,
                                                `status` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                                `goods_id` bigint(20) NOT NULL,
                                                `stock_check_order_id` bigint(20) NOT NULL,
                                                `team_id` bigint(20) NOT NULL,
                                                PRIMARY KEY (`id`) USING BTREE,
                                                UNIQUE INDEX `stock_check_stockcheckgo_stock_check_order_id_goo_f8f089dc_uniq`(`stock_check_order_id` ASC, `goods_id` ASC) USING BTREE,
                                                INDEX `stock_check_stockcheckgoods_goods_id_6ad71dc1_fk_goods_goods_id`(`goods_id` ASC) USING BTREE,
                                                INDEX `stock_check_stockcheckgoods_team_id_4320ecc1_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                                CONSTRAINT `stock_check_stockche_stock_check_order_id_60da3558_fk_stock_che` FOREIGN KEY (`stock_check_order_id`) REFERENCES `stock_check_stockcheckorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                CONSTRAINT `stock_check_stockcheckgoods_goods_id_6ad71dc1_fk_goods_goods_id` FOREIGN KEY (`goods_id`) REFERENCES `goods_goods` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                CONSTRAINT `stock_check_stockcheckgoods_team_id_4320ecc1_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of stock_check_stockcheckgoods
-- ----------------------------
INSERT INTO `stock_check_stockcheckgoods` VALUES (1, 200, 100, -100, 0, 0.00, 'loss', 6, 1, 5);
INSERT INTO `stock_check_stockcheckgoods` VALUES (2, 200, 20, -180, 0.5, -90.00, 'loss', 6, 2, 5);
INSERT INTO `stock_check_stockcheckgoods` VALUES (3, 20, 200, 180, 0.5, 90.00, 'surplus', 6, 3, 5);
INSERT INTO `stock_check_stockcheckgoods` VALUES (4, 200, 1000, 800, 0, 0.00, 'surplus', 7, 4, 5);

-- ----------------------------
-- Table structure for stock_check_stockcheckorder
-- ----------------------------
DROP TABLE IF EXISTS `stock_check_stockcheckorder`;
CREATE TABLE `stock_check_stockcheckorder`  (
                                                `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                                `number` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                                `handle_time` date NOT NULL,
                                                `remark` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                                `status` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                                `total_book_quantity` double NULL DEFAULT NULL,
                                                `total_actual_quantity` double NULL DEFAULT NULL,
                                                `total_surplus_quantity` double NULL DEFAULT NULL,
                                                `total_surplus_amount` decimal(16, 2) NULL DEFAULT NULL,
                                                `is_void` tinyint(1) NOT NULL,
                                                `create_time` datetime(6) NOT NULL,
                                                `creator_id` bigint(20) NOT NULL,
                                                `handler_id` bigint(20) NOT NULL,
                                                `team_id` bigint(20) NOT NULL,
                                                `warehouse_id` bigint(20) NOT NULL,
                                                PRIMARY KEY (`id`) USING BTREE,
                                                UNIQUE INDEX `stock_check_stockcheckorder_number_team_id_e9fc4f2d_uniq`(`number` ASC, `team_id` ASC) USING BTREE,
                                                INDEX `stock_check_stockche_creator_id_7300a8b9_fk_system_us`(`creator_id` ASC) USING BTREE,
                                                INDEX `stock_check_stockche_handler_id_dd9e007f_fk_system_us`(`handler_id` ASC) USING BTREE,
                                                INDEX `stock_check_stockcheckorder_team_id_293cc2e4_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                                INDEX `stock_check_stockche_warehouse_id_866949e0_fk_data_ware`(`warehouse_id` ASC) USING BTREE,
                                                CONSTRAINT `stock_check_stockche_creator_id_7300a8b9_fk_system_us` FOREIGN KEY (`creator_id`) REFERENCES `system_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                CONSTRAINT `stock_check_stockche_handler_id_dd9e007f_fk_system_us` FOREIGN KEY (`handler_id`) REFERENCES `system_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                CONSTRAINT `stock_check_stockche_warehouse_id_866949e0_fk_data_ware` FOREIGN KEY (`warehouse_id`) REFERENCES `data_warehouse` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                CONSTRAINT `stock_check_stockcheckorder_team_id_293cc2e4_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of stock_check_stockcheckorder
-- ----------------------------
INSERT INTO `stock_check_stockcheckorder` VALUES (1, 'PD202405170001', '2024-05-17', NULL, 'loss', 200, 100, -100, 0.00, 0, '2024-05-17 07:09:44.914075', 6, 6, 5, 4);
INSERT INTO `stock_check_stockcheckorder` VALUES (2, 'PD202405200001', '2024-04-30', NULL, 'loss', 200, 20, -180, -90.00, 0, '2024-05-20 10:40:18.530040', 6, 6, 5, 4);
INSERT INTO `stock_check_stockcheckorder` VALUES (3, 'PD202405200002', '2024-05-24', NULL, 'surplus', 20, 200, 180, 90.00, 0, '2024-05-20 10:40:45.460936', 6, 6, 5, 4);
INSERT INTO `stock_check_stockcheckorder` VALUES (4, 'PD202405200003', '2024-05-21', NULL, 'surplus', 200, 1000, 800, 0.00, 0, '2024-05-20 10:41:18.868139', 6, 6, 5, 4);

-- ----------------------------
-- Table structure for stock_in_stockingoods
-- ----------------------------
DROP TABLE IF EXISTS `stock_in_stockingoods`;
CREATE TABLE `stock_in_stockingoods`  (
                                          `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                          `stock_in_quantity` double NOT NULL,
                                          `remain_quantity` double NOT NULL,
                                          `is_completed` tinyint(1) NOT NULL,
                                          `goods_id` bigint(20) NOT NULL,
                                          `stock_in_order_id` bigint(20) NOT NULL,
                                          `team_id` bigint(20) NOT NULL,
                                          PRIMARY KEY (`id`) USING BTREE,
                                          UNIQUE INDEX `stock_in_stockingoods_stock_in_order_id_goods_id_47d0bdd3_uniq`(`stock_in_order_id` ASC, `goods_id` ASC) USING BTREE,
                                          INDEX `stock_in_stockingoods_goods_id_1f3806e9_fk_goods_goods_id`(`goods_id` ASC) USING BTREE,
                                          INDEX `stock_in_stockingoods_team_id_8854c3c6_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                          CONSTRAINT `stock_in_stockingood_stock_in_order_id_548bf799_fk_stock_in_` FOREIGN KEY (`stock_in_order_id`) REFERENCES `stock_in_stockinorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                          CONSTRAINT `stock_in_stockingoods_goods_id_1f3806e9_fk_goods_goods_id` FOREIGN KEY (`goods_id`) REFERENCES `goods_goods` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                          CONSTRAINT `stock_in_stockingoods_team_id_8854c3c6_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 27 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of stock_in_stockingoods
-- ----------------------------
INSERT INTO `stock_in_stockingoods` VALUES (10, 300, 0, 0, 6, 10, 5);
INSERT INTO `stock_in_stockingoods` VALUES (11, 200, 0, 0, 7, 10, 5);
INSERT INTO `stock_in_stockingoods` VALUES (12, 1000, 0, 0, 8, 11, 5);
INSERT INTO `stock_in_stockingoods` VALUES (13, 100, 0, 0, 6, 12, 5);
INSERT INTO `stock_in_stockingoods` VALUES (22, 300, 300, 0, 9, 17, 5);
INSERT INTO `stock_in_stockingoods` VALUES (23, 50, 50, 0, 9, 18, 5);
INSERT INTO `stock_in_stockingoods` VALUES (24, 3000, 3000, 0, 10, 19, 5);
INSERT INTO `stock_in_stockingoods` VALUES (25, 100, 100, 0, 15, 20, 5);
INSERT INTO `stock_in_stockingoods` VALUES (26, 50, 50, 0, 13, 21, 5);

-- ----------------------------
-- Table structure for stock_in_stockinorder
-- ----------------------------
DROP TABLE IF EXISTS `stock_in_stockinorder`;
CREATE TABLE `stock_in_stockinorder`  (
                                          `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                          `number` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                          `type` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                          `total_quantity` double NOT NULL,
                                          `remain_quantity` double NOT NULL,
                                          `is_completed` tinyint(1) NOT NULL,
                                          `is_void` tinyint(1) NOT NULL,
                                          `create_time` datetime(6) NOT NULL,
                                          `creator_id` bigint(20) NOT NULL,
                                          `purchase_order_id` bigint(20) NULL DEFAULT NULL,
                                          `sales_return_order_id` bigint(20) NULL DEFAULT NULL,
                                          `stock_transfer_order_id` bigint(20) NULL DEFAULT NULL,
                                          `team_id` bigint(20) NOT NULL,
                                          `warehouse_id` bigint(20) NOT NULL,
                                          PRIMARY KEY (`id`) USING BTREE,
                                          UNIQUE INDEX `stock_in_stockinorder_number_team_id_b3fb4e69_uniq`(`number` ASC, `team_id` ASC) USING BTREE,
                                          UNIQUE INDEX `purchase_order_id`(`purchase_order_id` ASC) USING BTREE,
                                          UNIQUE INDEX `sales_return_order_id`(`sales_return_order_id` ASC) USING BTREE,
                                          UNIQUE INDEX `stock_transfer_order_id`(`stock_transfer_order_id` ASC) USING BTREE,
                                          INDEX `stock_in_stockinorder_creator_id_43a02678_fk_system_user_id`(`creator_id` ASC) USING BTREE,
                                          INDEX `stock_in_stockinorder_team_id_a572150f_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                          INDEX `stock_in_stockinorder_warehouse_id_c445e3ad_fk_data_warehouse_id`(`warehouse_id` ASC) USING BTREE,
                                          CONSTRAINT `stock_in_stockinorde_purchase_order_id_4313cf0c_fk_purchase_` FOREIGN KEY (`purchase_order_id`) REFERENCES `purchase_purchaseorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                          CONSTRAINT `stock_in_stockinorde_sales_return_order_i_65ac07f0_fk_sales_sal` FOREIGN KEY (`sales_return_order_id`) REFERENCES `sales_salesreturnorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                          CONSTRAINT `stock_in_stockinorde_stock_transfer_order_79bd931b_fk_stock_tra` FOREIGN KEY (`stock_transfer_order_id`) REFERENCES `stock_transfer_stocktransferorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                          CONSTRAINT `stock_in_stockinorder_creator_id_43a02678_fk_system_user_id` FOREIGN KEY (`creator_id`) REFERENCES `system_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                          CONSTRAINT `stock_in_stockinorder_team_id_a572150f_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                          CONSTRAINT `stock_in_stockinorder_warehouse_id_c445e3ad_fk_data_warehouse_id` FOREIGN KEY (`warehouse_id`) REFERENCES `data_warehouse` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 22 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of stock_in_stockinorder
-- ----------------------------
INSERT INTO `stock_in_stockinorder` VALUES (10, 'RK202405170001', 'purchase', 500, 0, 1, 0, '2024-05-17 07:06:13.295761', 6, 15, NULL, NULL, 5, 4);
INSERT INTO `stock_in_stockinorder` VALUES (11, 'RK202406280001', 'purchase', 1000, 0, 1, 0, '2024-06-28 14:40:19.591669', 6, 16, NULL, NULL, 5, 4);
INSERT INTO `stock_in_stockinorder` VALUES (12, 'RK202406300001', 'sales_return', 100, 0, 1, 0, '2024-06-30 14:40:47.518301', 6, NULL, 3, NULL, 5, 4);
INSERT INTO `stock_in_stockinorder` VALUES (17, 'RK202407090001', 'purchase', 300, 300, 0, 0, '2024-07-09 02:38:11.994720', 6, 21, NULL, NULL, 5, 4);
INSERT INTO `stock_in_stockinorder` VALUES (18, 'RK202407100001', 'purchase', 50, 50, 0, 0, '2024-07-10 03:59:01.010153', 6, 22, NULL, NULL, 5, 6);
INSERT INTO `stock_in_stockinorder` VALUES (19, 'RK202407120001', 'purchase', 3000, 3000, 0, 0, '2024-07-12 13:38:25.290312', 6, 23, NULL, NULL, 5, 6);
INSERT INTO `stock_in_stockinorder` VALUES (20, 'RK202407190001', 'purchase', 100, 100, 0, 0, '2024-07-19 07:16:05.675217', 6, 24, NULL, NULL, 5, 4);
INSERT INTO `stock_in_stockinorder` VALUES (21, 'RK202407260001', 'purchase', 50, 50, 0, 0, '2024-07-25 16:43:56.212303', 6, 25, NULL, NULL, 5, 4);

-- ----------------------------
-- Table structure for stock_in_stockinrecord
-- ----------------------------
DROP TABLE IF EXISTS `stock_in_stockinrecord`;
CREATE TABLE `stock_in_stockinrecord`  (
                                           `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                           `handle_time` date NOT NULL,
                                           `remark` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                           `total_quantity` double NULL DEFAULT NULL,
                                           `is_void` tinyint(1) NOT NULL,
                                           `create_time` datetime(6) NOT NULL,
                                           `creator_id` bigint(20) NOT NULL,
                                           `handler_id` bigint(20) NOT NULL,
                                           `stock_in_order_id` bigint(20) NOT NULL,
                                           `team_id` bigint(20) NOT NULL,
                                           `warehouse_id` bigint(20) NOT NULL,
                                           PRIMARY KEY (`id`) USING BTREE,
                                           INDEX `stock_in_stockinrecord_creator_id_e8661061_fk_system_user_id`(`creator_id` ASC) USING BTREE,
                                           INDEX `stock_in_stockinrecord_handler_id_b240194b_fk_system_user_id`(`handler_id` ASC) USING BTREE,
                                           INDEX `stock_in_stockinreco_stock_in_order_id_e7019d41_fk_stock_in_`(`stock_in_order_id` ASC) USING BTREE,
                                           INDEX `stock_in_stockinrecord_team_id_d3c003af_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                           INDEX `stock_in_stockinreco_warehouse_id_8812d2f6_fk_data_ware`(`warehouse_id` ASC) USING BTREE,
                                           CONSTRAINT `stock_in_stockinreco_stock_in_order_id_e7019d41_fk_stock_in_` FOREIGN KEY (`stock_in_order_id`) REFERENCES `stock_in_stockinorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                           CONSTRAINT `stock_in_stockinreco_warehouse_id_8812d2f6_fk_data_ware` FOREIGN KEY (`warehouse_id`) REFERENCES `data_warehouse` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                           CONSTRAINT `stock_in_stockinrecord_creator_id_e8661061_fk_system_user_id` FOREIGN KEY (`creator_id`) REFERENCES `system_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                           CONSTRAINT `stock_in_stockinrecord_handler_id_b240194b_fk_system_user_id` FOREIGN KEY (`handler_id`) REFERENCES `system_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                           CONSTRAINT `stock_in_stockinrecord_team_id_d3c003af_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of stock_in_stockinrecord
-- ----------------------------
INSERT INTO `stock_in_stockinrecord` VALUES (8, '2024-05-17', NULL, 300, 0, '2024-05-17 07:07:15.447195', 6, 6, 10, 5, 4);
INSERT INTO `stock_in_stockinrecord` VALUES (9, '2024-05-17', NULL, 200, 0, '2024-05-17 07:07:52.502429', 6, 6, 10, 5, 4);
INSERT INTO `stock_in_stockinrecord` VALUES (10, '2024-07-06', NULL, 100, 0, '2024-07-06 18:23:28.209327', 6, 7, 12, 5, 4);
INSERT INTO `stock_in_stockinrecord` VALUES (11, '2024-07-08', NULL, 1000, 0, '2024-07-07 18:50:14.090449', 6, 7, 11, 5, 4);

-- ----------------------------
-- Table structure for stock_in_stockinrecordgoods
-- ----------------------------
DROP TABLE IF EXISTS `stock_in_stockinrecordgoods`;
CREATE TABLE `stock_in_stockinrecordgoods`  (
                                                `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                                `stock_in_quantity` double NOT NULL,
                                                `batch_id` bigint(20) NULL DEFAULT NULL,
                                                `goods_id` bigint(20) NOT NULL,
                                                `stock_in_goods_id` bigint(20) NOT NULL,
                                                `stock_in_record_id` bigint(20) NOT NULL,
                                                `team_id` bigint(20) NOT NULL,
                                                PRIMARY KEY (`id`) USING BTREE,
                                                UNIQUE INDEX `stock_in_stockinrecordgo_stock_in_record_id_goods_bd70d1b4_uniq`(`stock_in_record_id` ASC, `goods_id` ASC) USING BTREE,
                                                INDEX `stock_in_stockinrecordgoods_batch_id_72da4cd8_fk_goods_batch_id`(`batch_id` ASC) USING BTREE,
                                                INDEX `stock_in_stockinrecordgoods_goods_id_b8f34787_fk_goods_goods_id`(`goods_id` ASC) USING BTREE,
                                                INDEX `stock_in_stockinreco_stock_in_goods_id_0883ff23_fk_stock_in_`(`stock_in_goods_id` ASC) USING BTREE,
                                                INDEX `stock_in_stockinrecordgoods_team_id_2cd15879_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                                CONSTRAINT `stock_in_stockinreco_stock_in_goods_id_0883ff23_fk_stock_in_` FOREIGN KEY (`stock_in_goods_id`) REFERENCES `stock_in_stockingoods` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                CONSTRAINT `stock_in_stockinreco_stock_in_record_id_22e4e728_fk_stock_in_` FOREIGN KEY (`stock_in_record_id`) REFERENCES `stock_in_stockinrecord` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                CONSTRAINT `stock_in_stockinrecordgoods_batch_id_72da4cd8_fk_goods_batch_id` FOREIGN KEY (`batch_id`) REFERENCES `goods_batch` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                CONSTRAINT `stock_in_stockinrecordgoods_goods_id_b8f34787_fk_goods_goods_id` FOREIGN KEY (`goods_id`) REFERENCES `goods_goods` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                CONSTRAINT `stock_in_stockinrecordgoods_team_id_2cd15879_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 14 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of stock_in_stockinrecordgoods
-- ----------------------------
INSERT INTO `stock_in_stockinrecordgoods` VALUES (8, 200, NULL, 6, 10, 8, 5);
INSERT INTO `stock_in_stockinrecordgoods` VALUES (9, 100, NULL, 7, 11, 8, 5);
INSERT INTO `stock_in_stockinrecordgoods` VALUES (10, 100, NULL, 6, 10, 9, 5);
INSERT INTO `stock_in_stockinrecordgoods` VALUES (11, 100, NULL, 7, 11, 9, 5);
INSERT INTO `stock_in_stockinrecordgoods` VALUES (12, 100, NULL, 6, 13, 10, 5);
INSERT INTO `stock_in_stockinrecordgoods` VALUES (13, 1000, NULL, 8, 12, 11, 5);

-- ----------------------------
-- Table structure for stock_out_stockoutgoods
-- ----------------------------
DROP TABLE IF EXISTS `stock_out_stockoutgoods`;
CREATE TABLE `stock_out_stockoutgoods`  (
                                            `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                            `stock_out_quantity` double NOT NULL,
                                            `remain_quantity` double NOT NULL,
                                            `is_completed` tinyint(1) NOT NULL,
                                            `goods_id` bigint(20) NOT NULL,
                                            `stock_out_order_id` bigint(20) NOT NULL,
                                            `team_id` bigint(20) NOT NULL,
                                            PRIMARY KEY (`id`) USING BTREE,
                                            UNIQUE INDEX `stock_out_stockoutgoods_stock_out_order_id_goods_44597ba3_uniq`(`stock_out_order_id` ASC, `goods_id` ASC) USING BTREE,
                                            INDEX `stock_out_stockoutgoods_goods_id_a1703a52_fk_goods_goods_id`(`goods_id` ASC) USING BTREE,
                                            INDEX `stock_out_stockoutgoods_team_id_a178db46_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                            CONSTRAINT `stock_out_stockoutgo_stock_out_order_id_82010e3e_fk_stock_out` FOREIGN KEY (`stock_out_order_id`) REFERENCES `stock_out_stockoutorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                            CONSTRAINT `stock_out_stockoutgoods_goods_id_a1703a52_fk_goods_goods_id` FOREIGN KEY (`goods_id`) REFERENCES `goods_goods` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                            CONSTRAINT `stock_out_stockoutgoods_team_id_a178db46_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 15 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of stock_out_stockoutgoods
-- ----------------------------
INSERT INTO `stock_out_stockoutgoods` VALUES (9, 100, 0, 0, 6, 9, 5);
INSERT INTO `stock_out_stockoutgoods` VALUES (10, 1000, 1000, 0, 8, 10, 5);
INSERT INTO `stock_out_stockoutgoods` VALUES (11, 1, 1, 0, 8, 11, 5);
INSERT INTO `stock_out_stockoutgoods` VALUES (12, 222, 222, 0, 6, 12, 5);
INSERT INTO `stock_out_stockoutgoods` VALUES (13, 333, 333, 0, 7, 12, 5);
INSERT INTO `stock_out_stockoutgoods` VALUES (14, 1, 1, 0, 7, 13, 5);

-- ----------------------------
-- Table structure for stock_out_stockoutorder
-- ----------------------------
DROP TABLE IF EXISTS `stock_out_stockoutorder`;
CREATE TABLE `stock_out_stockoutorder`  (
                                            `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                            `number` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                            `type` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                            `total_quantity` double NOT NULL,
                                            `remain_quantity` double NOT NULL,
                                            `is_completed` tinyint(1) NOT NULL,
                                            `is_void` tinyint(1) NOT NULL,
                                            `create_time` datetime(6) NOT NULL,
                                            `creator_id` bigint(20) NOT NULL,
                                            `purchase_return_order_id` bigint(20) NULL DEFAULT NULL,
                                            `sales_order_id` bigint(20) NULL DEFAULT NULL,
                                            `stock_transfer_order_id` bigint(20) NULL DEFAULT NULL,
                                            `team_id` bigint(20) NOT NULL,
                                            `warehouse_id` bigint(20) NOT NULL,
                                            PRIMARY KEY (`id`) USING BTREE,
                                            UNIQUE INDEX `stock_out_stockoutorder_number_team_id_3163c9fa_uniq`(`number` ASC, `team_id` ASC) USING BTREE,
                                            UNIQUE INDEX `purchase_return_order_id`(`purchase_return_order_id` ASC) USING BTREE,
                                            UNIQUE INDEX `sales_order_id`(`sales_order_id` ASC) USING BTREE,
                                            UNIQUE INDEX `stock_transfer_order_id`(`stock_transfer_order_id` ASC) USING BTREE,
                                            INDEX `stock_out_stockoutorder_creator_id_a2085303_fk_system_user_id`(`creator_id` ASC) USING BTREE,
                                            INDEX `stock_out_stockoutorder_team_id_1dbd8fe7_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                            INDEX `stock_out_stockoutor_warehouse_id_b9b48d54_fk_data_ware`(`warehouse_id` ASC) USING BTREE,
                                            CONSTRAINT `stock_out_stockoutor_purchase_return_orde_3c4818aa_fk_purchase_` FOREIGN KEY (`purchase_return_order_id`) REFERENCES `purchase_purchasereturnorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                            CONSTRAINT `stock_out_stockoutor_sales_order_id_a3af463e_fk_sales_sal` FOREIGN KEY (`sales_order_id`) REFERENCES `sales_salesorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                            CONSTRAINT `stock_out_stockoutor_stock_transfer_order_e937eb98_fk_stock_tra` FOREIGN KEY (`stock_transfer_order_id`) REFERENCES `stock_transfer_stocktransferorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                            CONSTRAINT `stock_out_stockoutor_warehouse_id_b9b48d54_fk_data_ware` FOREIGN KEY (`warehouse_id`) REFERENCES `data_warehouse` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                            CONSTRAINT `stock_out_stockoutorder_creator_id_a2085303_fk_system_user_id` FOREIGN KEY (`creator_id`) REFERENCES `system_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                            CONSTRAINT `stock_out_stockoutorder_team_id_1dbd8fe7_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 14 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of stock_out_stockoutorder
-- ----------------------------
INSERT INTO `stock_out_stockoutorder` VALUES (9, 'CK202405170001', 'sales', 100, 0, 1, 0, '2024-05-17 07:08:53.612339', 6, NULL, 14, NULL, 5, 4);
INSERT INTO `stock_out_stockoutorder` VALUES (10, 'CK202406300001', 'purchase', 1000, 1000, 0, 0, '2024-06-30 14:14:25.226708', 6, 2, NULL, NULL, 5, 4);
INSERT INTO `stock_out_stockoutorder` VALUES (11, 'CK202406300002', 'sales', 1, 1, 0, 1, '2024-06-30 14:30:55.330451', 6, NULL, 15, NULL, 5, 4);
INSERT INTO `stock_out_stockoutorder` VALUES (12, 'CK202407070001', 'sales', 555, 555, 0, 0, '2024-07-06 18:30:47.741009', 6, NULL, 16, NULL, 5, 4);
INSERT INTO `stock_out_stockoutorder` VALUES (13, 'CK202407290001', 'sales', 1, 1, 0, 0, '2024-07-29 06:57:08.482731', 6, NULL, 17, NULL, 5, 4);

-- ----------------------------
-- Table structure for stock_out_stockoutrecord
-- ----------------------------
DROP TABLE IF EXISTS `stock_out_stockoutrecord`;
CREATE TABLE `stock_out_stockoutrecord`  (
                                             `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                             `handle_time` date NOT NULL,
                                             `remark` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                             `total_quantity` double NULL DEFAULT NULL,
                                             `is_void` tinyint(1) NOT NULL,
                                             `create_time` datetime(6) NOT NULL,
                                             `creator_id` bigint(20) NOT NULL,
                                             `handler_id` bigint(20) NOT NULL,
                                             `stock_out_order_id` bigint(20) NOT NULL,
                                             `team_id` bigint(20) NOT NULL,
                                             `warehouse_id` bigint(20) NOT NULL,
                                             PRIMARY KEY (`id`) USING BTREE,
                                             INDEX `stock_out_stockoutrecord_creator_id_ff6c64dd_fk_system_user_id`(`creator_id` ASC) USING BTREE,
                                             INDEX `stock_out_stockoutrecord_handler_id_c01e4efb_fk_system_user_id`(`handler_id` ASC) USING BTREE,
                                             INDEX `stock_out_stockoutre_stock_out_order_id_106c8ed1_fk_stock_out`(`stock_out_order_id` ASC) USING BTREE,
                                             INDEX `stock_out_stockoutrecord_team_id_58dd46fd_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                             INDEX `stock_out_stockoutre_warehouse_id_d45f77e5_fk_data_ware`(`warehouse_id` ASC) USING BTREE,
                                             CONSTRAINT `stock_out_stockoutre_stock_out_order_id_106c8ed1_fk_stock_out` FOREIGN KEY (`stock_out_order_id`) REFERENCES `stock_out_stockoutorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                             CONSTRAINT `stock_out_stockoutre_warehouse_id_d45f77e5_fk_data_ware` FOREIGN KEY (`warehouse_id`) REFERENCES `data_warehouse` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                             CONSTRAINT `stock_out_stockoutrecord_creator_id_ff6c64dd_fk_system_user_id` FOREIGN KEY (`creator_id`) REFERENCES `system_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                             CONSTRAINT `stock_out_stockoutrecord_handler_id_c01e4efb_fk_system_user_id` FOREIGN KEY (`handler_id`) REFERENCES `system_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                             CONSTRAINT `stock_out_stockoutrecord_team_id_58dd46fd_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of stock_out_stockoutrecord
-- ----------------------------
INSERT INTO `stock_out_stockoutrecord` VALUES (3, '2024-05-17', NULL, 100, 0, '2024-05-17 07:09:17.206251', 6, 6, 9, 5, 4);

-- ----------------------------
-- Table structure for stock_out_stockoutrecordgoods
-- ----------------------------
DROP TABLE IF EXISTS `stock_out_stockoutrecordgoods`;
CREATE TABLE `stock_out_stockoutrecordgoods`  (
                                                  `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                                  `stock_out_quantity` double NOT NULL,
                                                  `batch_id` bigint(20) NULL DEFAULT NULL,
                                                  `goods_id` bigint(20) NOT NULL,
                                                  `stock_out_goods_id` bigint(20) NOT NULL,
                                                  `stock_out_record_id` bigint(20) NOT NULL,
                                                  `team_id` bigint(20) NOT NULL,
                                                  PRIMARY KEY (`id`) USING BTREE,
                                                  UNIQUE INDEX `stock_out_stockoutrecord_stock_out_record_id_good_82d77178_uniq`(`stock_out_record_id` ASC, `goods_id` ASC) USING BTREE,
                                                  INDEX `stock_out_stockoutre_batch_id_12d3f06a_fk_goods_bat`(`batch_id` ASC) USING BTREE,
                                                  INDEX `stock_out_stockoutre_goods_id_43f08fcc_fk_goods_goo`(`goods_id` ASC) USING BTREE,
                                                  INDEX `stock_out_stockoutre_stock_out_goods_id_763a059e_fk_stock_out`(`stock_out_goods_id` ASC) USING BTREE,
                                                  INDEX `stock_out_stockoutrecordgoods_team_id_54e90ef8_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                                  CONSTRAINT `stock_out_stockoutre_batch_id_12d3f06a_fk_goods_bat` FOREIGN KEY (`batch_id`) REFERENCES `goods_batch` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                  CONSTRAINT `stock_out_stockoutre_goods_id_43f08fcc_fk_goods_goo` FOREIGN KEY (`goods_id`) REFERENCES `goods_goods` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                  CONSTRAINT `stock_out_stockoutre_stock_out_goods_id_763a059e_fk_stock_out` FOREIGN KEY (`stock_out_goods_id`) REFERENCES `stock_out_stockoutgoods` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                  CONSTRAINT `stock_out_stockoutre_stock_out_record_id_061c8efb_fk_stock_out` FOREIGN KEY (`stock_out_record_id`) REFERENCES `stock_out_stockoutrecord` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                  CONSTRAINT `stock_out_stockoutrecordgoods_team_id_54e90ef8_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of stock_out_stockoutrecordgoods
-- ----------------------------
INSERT INTO `stock_out_stockoutrecordgoods` VALUES (3, 100, NULL, 6, 9, 3, 5);

-- ----------------------------
-- Table structure for stock_transfer_stocktransfergoods
-- ----------------------------
DROP TABLE IF EXISTS `stock_transfer_stocktransfergoods`;
CREATE TABLE `stock_transfer_stocktransfergoods`  (
                                                      `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                                      `stock_transfer_quantity` double NOT NULL,
                                                      `goods_id` bigint(20) NOT NULL,
                                                      `stock_transfer_order_id` bigint(20) NOT NULL,
                                                      `team_id` bigint(20) NOT NULL,
                                                      PRIMARY KEY (`id`) USING BTREE,
                                                      UNIQUE INDEX `stock_transfer_stocktran_stock_transfer_order_id__14e6599d_uniq`(`stock_transfer_order_id` ASC, `goods_id` ASC) USING BTREE,
                                                      INDEX `stock_transfer_stock_goods_id_3abc55e5_fk_goods_goo`(`goods_id` ASC) USING BTREE,
                                                      INDEX `stock_transfer_stock_team_id_23508926_fk_system_te`(`team_id` ASC) USING BTREE,
                                                      CONSTRAINT `stock_transfer_stock_goods_id_3abc55e5_fk_goods_goo` FOREIGN KEY (`goods_id`) REFERENCES `goods_goods` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                      CONSTRAINT `stock_transfer_stock_stock_transfer_order_19bf1229_fk_stock_tra` FOREIGN KEY (`stock_transfer_order_id`) REFERENCES `stock_transfer_stocktransferorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                      CONSTRAINT `stock_transfer_stock_team_id_23508926_fk_system_te` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of stock_transfer_stocktransfergoods
-- ----------------------------

-- ----------------------------
-- Table structure for stock_transfer_stocktransferorder
-- ----------------------------
DROP TABLE IF EXISTS `stock_transfer_stocktransferorder`;
CREATE TABLE `stock_transfer_stocktransferorder`  (
                                                      `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                                      `number` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                                      `handle_time` date NOT NULL,
                                                      `remark` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                                      `total_quantity` double NULL DEFAULT NULL,
                                                      `is_void` tinyint(1) NOT NULL,
                                                      `enable_auto_stock_out` tinyint(1) NOT NULL,
                                                      `enable_auto_stock_in` tinyint(1) NOT NULL,
                                                      `create_time` datetime(6) NOT NULL,
                                                      `creator_id` bigint(20) NOT NULL,
                                                      `handler_id` bigint(20) NOT NULL,
                                                      `in_warehouse_id` bigint(20) NOT NULL,
                                                      `out_warehouse_id` bigint(20) NOT NULL,
                                                      `team_id` bigint(20) NOT NULL,
                                                      PRIMARY KEY (`id`) USING BTREE,
                                                      UNIQUE INDEX `stock_transfer_stocktransferorder_number_team_id_f371251a_uniq`(`number` ASC, `team_id` ASC) USING BTREE,
                                                      INDEX `stock_transfer_stock_creator_id_4764cbff_fk_system_us`(`creator_id` ASC) USING BTREE,
                                                      INDEX `stock_transfer_stock_handler_id_7f0a4e15_fk_system_us`(`handler_id` ASC) USING BTREE,
                                                      INDEX `stock_transfer_stock_in_warehouse_id_10bd7d5f_fk_data_ware`(`in_warehouse_id` ASC) USING BTREE,
                                                      INDEX `stock_transfer_stock_out_warehouse_id_7242f8b5_fk_data_ware`(`out_warehouse_id` ASC) USING BTREE,
                                                      INDEX `stock_transfer_stock_team_id_cbb65d1f_fk_system_te`(`team_id` ASC) USING BTREE,
                                                      CONSTRAINT `stock_transfer_stock_creator_id_4764cbff_fk_system_us` FOREIGN KEY (`creator_id`) REFERENCES `system_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                      CONSTRAINT `stock_transfer_stock_handler_id_7f0a4e15_fk_system_us` FOREIGN KEY (`handler_id`) REFERENCES `system_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                      CONSTRAINT `stock_transfer_stock_in_warehouse_id_10bd7d5f_fk_data_ware` FOREIGN KEY (`in_warehouse_id`) REFERENCES `data_warehouse` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                      CONSTRAINT `stock_transfer_stock_out_warehouse_id_7242f8b5_fk_data_ware` FOREIGN KEY (`out_warehouse_id`) REFERENCES `data_warehouse` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                                      CONSTRAINT `stock_transfer_stock_team_id_cbb65d1f_fk_system_te` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of stock_transfer_stocktransferorder
-- ----------------------------

-- ----------------------------
-- Table structure for system_permission
-- ----------------------------
DROP TABLE IF EXISTS `system_permission`;
CREATE TABLE `system_permission`  (
                                      `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                      `name` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                      `code` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                      `group_id` bigint(20) NOT NULL,
                                      PRIMARY KEY (`id`) USING BTREE,
                                      INDEX `system_permission_group_id_3e12b055_fk_system_permissiongroup_id`(`group_id` ASC) USING BTREE,
                                      CONSTRAINT `system_permission_group_id_3e12b055_fk_system_permissiongroup_id` FOREIGN KEY (`group_id`) REFERENCES `system_permissiongroup` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 37 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of system_permission
-- ----------------------------
INSERT INTO `system_permission` VALUES (1, '销售走势', 'sales_trend', 10);
INSERT INTO `system_permission` VALUES (2, '销售前十产品', 'sales_hot_goods', 10);
INSERT INTO `system_permission` VALUES (3, '入库任务提醒', 'stock_in_reminder', 10);
INSERT INTO `system_permission` VALUES (4, '出库任务提醒', 'stock_out_reminder', 10);
INSERT INTO `system_permission` VALUES (5, '库存预警', 'inventory_warning', 10);
INSERT INTO `system_permission` VALUES (6, '销售报表', 'sales_report', 11);
INSERT INTO `system_permission` VALUES (7, '采购报表', 'purchase_report', 11);
INSERT INTO `system_permission` VALUES (8, '库存报表', 'inventory', 11);
INSERT INTO `system_permission` VALUES (9, '批次报表', 'batch', 11);
INSERT INTO `system_permission` VALUES (10, '收支统计', 'finance_statistic', 11);
INSERT INTO `system_permission` VALUES (11, '客户管理', 'client', 12);
INSERT INTO `system_permission` VALUES (12, '供应商管理', 'supplier', 12);
INSERT INTO `system_permission` VALUES (13, '仓库管理', 'warehouse', 12);
INSERT INTO `system_permission` VALUES (14, '结算账户', 'account', 12);
INSERT INTO `system_permission` VALUES (15, '收支项目', 'charge_item', 12);
INSERT INTO `system_permission` VALUES (16, '产品分类', 'goods_category', 13);
INSERT INTO `system_permission` VALUES (17, '产品单位', 'goods_unit', 13);
INSERT INTO `system_permission` VALUES (18, '产品信息', 'goods', 13);
INSERT INTO `system_permission` VALUES (19, '采购开单', 'purchase_order', 14);
INSERT INTO `system_permission` VALUES (20, '采购退货', 'purchase_return_order', 14);
INSERT INTO `system_permission` VALUES (21, '销售开单', 'sales_order', 15);
INSERT INTO `system_permission` VALUES (22, '销售退货', 'sales_return_order', 15);
INSERT INTO `system_permission` VALUES (23, '生产计划', 'production_order', 16);
INSERT INTO `system_permission` VALUES (24, '生产记录', 'production_record', 16);
INSERT INTO `system_permission` VALUES (25, '入库', 'stock_in', 17);
INSERT INTO `system_permission` VALUES (26, '出库', 'stock_out', 17);
INSERT INTO `system_permission` VALUES (27, '盘点', 'stock_check', 17);
INSERT INTO `system_permission` VALUES (28, '调拨', 'stock_transfer', 17);
INSERT INTO `system_permission` VALUES (29, '库存流水', 'inventory_flow', 17);
INSERT INTO `system_permission` VALUES (30, '应付欠款', 'supplier_arrears', 18);
INSERT INTO `system_permission` VALUES (31, '付款', 'payment_order', 18);
INSERT INTO `system_permission` VALUES (32, '应收欠款', 'client_arrears', 18);
INSERT INTO `system_permission` VALUES (33, '收款', 'collection_order', 18);
INSERT INTO `system_permission` VALUES (34, '账户转账', 'account_transfer_record', 18);
INSERT INTO `system_permission` VALUES (35, '日常收支', 'charge_order', 18);
INSERT INTO `system_permission` VALUES (36, '资金流水', 'finance_flow', 18);

-- ----------------------------
-- Table structure for system_permissiongroup
-- ----------------------------
DROP TABLE IF EXISTS `system_permissiongroup`;
CREATE TABLE `system_permissiongroup`  (
                                           `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                           `name` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                           PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 19 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of system_permissiongroup
-- ----------------------------
INSERT INTO `system_permissiongroup` VALUES (10, '首页');
INSERT INTO `system_permissiongroup` VALUES (11, '报表统计');
INSERT INTO `system_permissiongroup` VALUES (12, '基础数据');
INSERT INTO `system_permissiongroup` VALUES (13, '产品管理');
INSERT INTO `system_permissiongroup` VALUES (14, '采购管理');
INSERT INTO `system_permissiongroup` VALUES (15, '销售管理');
INSERT INTO `system_permissiongroup` VALUES (16, '生产管理');
INSERT INTO `system_permissiongroup` VALUES (17, '库内管理');
INSERT INTO `system_permissiongroup` VALUES (18, '财务管理');

-- ----------------------------
-- Table structure for system_role
-- ----------------------------
DROP TABLE IF EXISTS `system_role`;
CREATE TABLE `system_role`  (
                                `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                `name` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                `remark` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                `team_id` bigint(20) NOT NULL,
                                PRIMARY KEY (`id`) USING BTREE,
                                UNIQUE INDEX `system_role_name_team_id_50c42b8d_uniq`(`name` ASC, `team_id` ASC) USING BTREE,
                                INDEX `system_role_team_id_5acae71f_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                CONSTRAINT `system_role_team_id_5acae71f_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of system_role
-- ----------------------------
INSERT INTO `system_role` VALUES (7, '啊啊啊', NULL, 5);
INSERT INTO `system_role` VALUES (8, '员工', NULL, 5);

-- ----------------------------
-- Table structure for system_role_permissions
-- ----------------------------
DROP TABLE IF EXISTS `system_role_permissions`;
CREATE TABLE `system_role_permissions`  (
                                            `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                            `role_id` bigint(20) NOT NULL,
                                            `permission_id` bigint(20) NOT NULL,
                                            PRIMARY KEY (`id`) USING BTREE,
                                            UNIQUE INDEX `system_role_permissions_role_id_permission_id_084b6a64_uniq`(`role_id` ASC, `permission_id` ASC) USING BTREE,
                                            INDEX `system_role_permissi_permission_id_966ab5d8_fk_system_pe`(`permission_id` ASC) USING BTREE,
                                            CONSTRAINT `system_role_permissi_permission_id_966ab5d8_fk_system_pe` FOREIGN KEY (`permission_id`) REFERENCES `system_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                            CONSTRAINT `system_role_permissions_role_id_a52abc64_fk_system_role_id` FOREIGN KEY (`role_id`) REFERENCES `system_role` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 92 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of system_role_permissions
-- ----------------------------
INSERT INTO `system_role_permissions` VALUES (73, 7, 13);
INSERT INTO `system_role_permissions` VALUES (74, 8, 19);
INSERT INTO `system_role_permissions` VALUES (75, 8, 20);
INSERT INTO `system_role_permissions` VALUES (76, 8, 21);
INSERT INTO `system_role_permissions` VALUES (77, 8, 22);
INSERT INTO `system_role_permissions` VALUES (78, 8, 25);
INSERT INTO `system_role_permissions` VALUES (79, 8, 26);
INSERT INTO `system_role_permissions` VALUES (80, 8, 27);
INSERT INTO `system_role_permissions` VALUES (81, 8, 28);
INSERT INTO `system_role_permissions` VALUES (82, 8, 29);

-- ----------------------------
-- Table structure for system_team
-- ----------------------------
DROP TABLE IF EXISTS `system_team`;
CREATE TABLE `system_team`  (
                                `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                `number` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                `expiry_time` datetime(6) NOT NULL,
                                `create_time` datetime(6) NOT NULL,
                                `user_quantity` int(11) NOT NULL,
                                `remark` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                `enable_auto_stock_in` tinyint(1) NOT NULL,
                                `enable_auto_stock_out` tinyint(1) NOT NULL,
                                PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of system_team
-- ----------------------------
INSERT INTO `system_team` VALUES (3, '2', '2024-02-24 04:47:50.881350', '2023-11-16 04:47:51.332005', 10, NULL, 0, 0);
INSERT INTO `system_team` VALUES (4, '11', '2051-10-02 14:32:15.350599', '2024-05-16 14:32:15.397490', 10, NULL, 0, 0);
INSERT INTO `system_team` VALUES (5, '2', '2298-03-01 14:33:34.147039', '2024-05-16 14:33:34.191663', 10, NULL, 0, 0);
INSERT INTO `system_team` VALUES (6, '2', '2024-11-11 13:37:28.123517', '2024-08-03 13:37:28.153511', 10, NULL, 0, 0);
INSERT INTO `system_team` VALUES (7, '2', '2051-12-20 13:45:09.263576', '2024-08-03 13:45:09.289035', 10, NULL, 0, 0);
INSERT INTO `system_team` VALUES (8, '2', '2051-12-20 13:46:43.073938', '2024-08-03 13:46:43.102761', 10, NULL, 0, 0);

-- ----------------------------
-- Table structure for system_user
-- ----------------------------
DROP TABLE IF EXISTS `system_user`;
CREATE TABLE `system_user`  (
                                `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                `username` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                `password` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                `name` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                `phone` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                `email` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                                `sex` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                `permissions` json NOT NULL,
                                `is_manager` tinyint(1) NOT NULL,
                                `is_active` tinyint(1) NOT NULL,
                                `create_time` datetime(6) NOT NULL,
                                `team_id` bigint(20) NOT NULL,
                                PRIMARY KEY (`id`) USING BTREE,
                                UNIQUE INDEX `system_user_username_team_id_11850b48_uniq`(`username` ASC, `team_id` ASC) USING BTREE,
                                UNIQUE INDEX `system_user_name_team_id_c3bfb516_uniq`(`name` ASC, `team_id` ASC) USING BTREE,
                                INDEX `system_user_team_id_bfe9429c_fk_system_team_id`(`team_id` ASC) USING BTREE,
                                CONSTRAINT `system_user_team_id_bfe9429c_fk_system_team_id` FOREIGN KEY (`team_id`) REFERENCES `system_team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of system_user
-- ----------------------------
INSERT INTO `system_user` VALUES (2, '管理员\'', 'pbkdf2_sha256$260000$oGLHEHQZgqxXhXOn8Vex1x$vxZksva2P7xHUO2U1sa46x/QZrnmUzdHPTjCD/Tf3wI=', '管理员', NULL, NULL, '', '[]', 1, 1, '2023-11-16 04:47:51.453081', 3);
INSERT INTO `system_user` VALUES (5, '管理员', 'pbkdf2_sha256$260000$lxSV82XPBecS34cLooDs2y$rG3xUI/oT8rsE0BBryW2SP9f6usWWFBQy0CmfpTRqRc=', 'gu', NULL, NULL, '', '[]', 1, 1, '2024-05-16 14:32:15.708291', 4);
INSERT INTO `system_user` VALUES (6, '管理员', 'pbkdf2_sha256$260000$RnvGvJ33fHCgFD0UDWUJ9M$y/059QZ2sZeuXu9O4qniUZ0OlgsptIE1yJffFQUGJJs=', '管理员', NULL, NULL, '', '[]', 1, 1, '2024-05-16 14:33:34.472247', 5);
INSERT INTO `system_user` VALUES (7, '22', 'pbkdf2_sha256$260000$vV94K4mqHT0dNbsv0ZxPEc$YXAhyqRHp5nNHiAgjNnYtK3INuoHSqkfWvshMzj6JDY=', '22', '22', '22', 'woman', '[\"warehouse\"]', 0, 1, '2024-05-21 02:57:08.485588', 5);
INSERT INTO `system_user` VALUES (8, 'zzz', 'pbkdf2_sha256$260000$gcTDLESUXzFRJDGXyHU7Vu$SFv/hv+iRYD8tLDL+yN/QA9JSxPvdk6PN6qtVXt/tFI=', '张三', '123333333', '122222222', 'man', '[\"purchase_order\", \"sales_order\", \"stock_out\", \"purchase_return_order\", \"sales_return_order\", \"stock_transfer\", \"inventory_flow\", \"stock_in\", \"stock_check\"]', 0, 1, '2024-06-28 08:51:20.048383', 5);
INSERT INTO `system_user` VALUES (9, 'name', 'pbkdf2_sha256$260000$vyfskKK4irVv8OaK1bTfzf$XnLoBniDAPqLr3tHN3OqI8FbT7053CiGs6qGQzNmv7I=', 'name', NULL, NULL, 'man', '[]', 0, 1, '2024-08-01 07:32:22.202258', 5);
INSERT INTO `system_user` VALUES (10, 'admin', 'pbkdf2_sha256$260000$unbhqsoGqbtgz4yhubmk3c$ef/08VVs5+mxuzTipLttx/jWqU4wxnYKXl8ax225Qro=', 'admin', NULL, NULL, '', '[]', 1, 1, '2024-08-03 13:37:28.306002', 6);
INSERT INTO `system_user` VALUES (11, '管理员', 'pbkdf2_sha256$260000$nH6U5oSsTspMsEF96mtczE$X/W940UGrz85KCd13G2UHNKkm2KAKURq6qKQCCPkl68=', '管理员', NULL, NULL, '', '[]', 1, 1, '2024-08-03 13:45:09.401455', 7);
INSERT INTO `system_user` VALUES (12, '管理员', 'pbkdf2_sha256$260000$8qdcv5DggmEfSWrwnaGUd7$PHaKNm014fCE0P/k+u3toG7Z+p4rMIzB5C9vMbeddaA=', '管理员', NULL, NULL, '', '[]', 1, 1, '2024-08-03 13:46:43.211720', 8);

-- ----------------------------
-- Table structure for system_user_roles
-- ----------------------------
DROP TABLE IF EXISTS `system_user_roles`;
CREATE TABLE `system_user_roles`  (
                                      `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                      `user_id` bigint(20) NOT NULL,
                                      `role_id` bigint(20) NOT NULL,
                                      PRIMARY KEY (`id`) USING BTREE,
                                      UNIQUE INDEX `system_user_roles_user_id_role_id_3e1bc63a_uniq`(`user_id` ASC, `role_id` ASC) USING BTREE,
                                      INDEX `system_user_roles_role_id_b1460da7_fk_system_role_id`(`role_id` ASC) USING BTREE,
                                      CONSTRAINT `system_user_roles_role_id_b1460da7_fk_system_role_id` FOREIGN KEY (`role_id`) REFERENCES `system_role` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
                                      CONSTRAINT `system_user_roles_user_id_a8e0376b_fk_system_user_id` FOREIGN KEY (`user_id`) REFERENCES `system_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of system_user_roles
-- ----------------------------
INSERT INTO `system_user_roles` VALUES (7, 7, 7);
INSERT INTO `system_user_roles` VALUES (8, 8, 8);

SET FOREIGN_KEY_CHECKS = 1;
