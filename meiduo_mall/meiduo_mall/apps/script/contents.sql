-- MySQL dump 10.13  Distrib 5.7.24, for Linux (x86_64)
--
-- Host: localhost    Database: meiduo_mis_db
-- ------------------------------------------------------
-- Server version	5.7.24-0ubuntu0.16.04.1-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `tb_content_category`
--

DROP TABLE IF EXISTS `tb_content_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_content_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `name` varchar(50) NOT NULL,
  `key` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_content_category`
--

LOCK TABLES `tb_content_category` WRITE;
/*!40000 ALTER TABLE `tb_content_category` DISABLE KEYS */;
INSERT INTO `tb_content_category` VALUES (1,'2018-04-09 16:04:47.411368','2018-04-09 16:15:26.439825','轮播图','index_lbt'),(2,'2018-04-09 16:06:12.495372','2018-04-09 16:15:32.385060','快讯','index_kx'),(3,'2018-04-09 16:08:36.725277','2018-04-09 16:15:39.930440','页头广告','index_ytgg'),(5,'2018-04-09 16:16:47.531007','2018-04-09 16:16:47.531082','1楼Logo','index_1f_logo'),(6,'2018-04-09 16:17:49.114299','2018-04-09 16:17:49.114342','1楼频道','index_1f_pd'),(7,'2018-04-09 16:18:04.659549','2018-04-09 16:18:04.659588','1楼标签','index_1f_bq'),(8,'2018-04-09 16:18:36.176926','2018-04-09 16:18:36.176991','1楼时尚新品','index_1f_ssxp'),(10,'2018-04-09 16:19:24.489532','2018-04-10 09:49:38.621008','1楼畅享低价','index_1f_cxdj'),(11,'2018-04-09 16:19:46.992482','2018-04-09 16:19:46.992525','1楼手机配件','index_1f_sjpj'),(13,'2018-04-09 16:20:32.331884','2018-04-09 16:20:32.331927','2楼Logo','index_2f_logo'),(14,'2018-04-09 16:20:46.334441','2018-04-09 16:20:46.334481','2楼频道','index_2f_pd'),(15,'2018-04-09 16:21:04.265294','2018-04-09 16:21:04.265336','2楼标签','index_2f_bq'),(16,'2018-04-09 16:21:22.869586','2018-04-10 09:51:49.310917','2楼加价换够','index_2f_jjhg'),(18,'2018-04-09 16:21:59.579570','2018-04-10 09:49:44.891002','2楼畅享低价','index_2f_cxdj'),(21,'2018-04-09 16:22:43.365608','2018-04-09 16:22:43.365653','3楼Logo','index_3f_logo'),(22,'2018-04-09 16:22:55.358798','2018-04-09 16:22:55.358856','3楼频道','index_3f_pd'),(23,'2018-04-09 16:23:05.211747','2018-04-09 16:23:05.211785','3楼标签','index_3f_bq'),(24,'2018-04-09 16:24:01.858753','2018-04-09 16:24:01.858803','3楼生活用品','index_3f_shyp'),(25,'2018-04-09 16:24:17.621898','2018-04-09 16:24:17.621942','3楼厨房用品','index_3f_cfyp');
/*!40000 ALTER TABLE `tb_content_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_content`
--

DROP TABLE IF EXISTS `tb_content`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_content` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `title` varchar(100) NOT NULL,
  `url` varchar(300) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `text` longtext,
  `sequence` int(11) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `category_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tb_content_category_id_c6e5ac73_fk_tb_content_category_id` (`category_id`),
  CONSTRAINT `tb_content_category_id_c6e5ac73_fk_tb_content_category_id` FOREIGN KEY (`category_id`) REFERENCES `tb_content_category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=124 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_content`
--

LOCK TABLES `tb_content` WRITE;
/*!40000 ALTER TABLE `tb_content` DISABLE KEYS */;
INSERT INTO `tb_content` VALUES (1,'2018-04-09 16:50:23.230734','2018-04-09 16:50:23.230780','美图M8s','http://www.itcast.cn','group1/M00/00/01/CtM3BVrLmc-AJdVSAAEI5Wm7zaw8639396','',1,1,1),(2,'2018-04-09 16:51:46.173309','2018-04-09 16:51:46.173354','黑色星期五','http://www.itcast.cn','group1/M00/00/01/CtM3BVrLmiKANEeLAAFfMRWFbY86177278','',2,1,1),(3,'2018-04-09 16:52:22.471123','2018-04-09 16:52:22.471191','厨卫365','http://www.itcast.cn','group1/M00/00/01/CtM3BVrLmkaAPIMJAAESCG7GAh43642702','',3,1,1),(4,'2018-04-09 16:53:10.539505','2018-04-09 16:53:10.539553','君乐宝买一送一','http://www.itcast.cn','group1/M00/00/01/CtM3BVrLmnaADtSKAAGlxZuk7uk4998927','',4,1,1),(5,'2018-04-09 16:53:57.409847','2018-04-09 16:53:57.409913','i7顽石低至4199元','http://www.itcast.cn','','',1,1,2),(6,'2018-04-09 16:54:36.805870','2018-04-09 16:54:36.805912','奥克斯专场 正1匹空调1313元抢','http://www.itcast.cn','','',2,1,2),(7,'2018-04-09 16:55:37.481628','2018-04-09 16:55:37.481707','荣耀9青春版 高配 领券立减220元','http://www.itcast.cn','','',3,1,2),(8,'2018-04-09 16:55:59.644645','2018-04-09 16:55:59.644697','美多探索公益新模式','http://www.itcast.cn','','',4,1,2),(9,'2018-04-09 16:57:05.390017','2018-04-09 16:57:05.390098','冰箱洗衣机专场 套购9折','http://www.itcast.cn','','',5,1,2),(10,'2018-04-09 16:57:41.680151','2018-04-09 16:57:41.680198','超市美食家 满188减100','http://www.itcast.cn','','',6,1,2),(11,'2018-04-09 16:58:27.074643','2018-04-09 16:58:27.074831','电竟之日 电脑最高减1000元','http://www.itcast.cn','','',7,1,2),(12,'2018-04-09 16:59:36.669624','2018-04-09 16:59:36.669664','好友联盟双双赚','http://www.itcast.cn','group1/M00/00/01/CtM3BVrLm_iAILnwAACbl1lbG3U8255973','',1,1,3),(14,'2018-04-09 17:01:42.028961','2018-04-09 17:01:42.029005','荣耀V10','http://www.itcast.cn','group1/M00/00/01/CtM3BVrLnHaATJWfAABcalxfbWk5995788','',1,1,5),(15,'2018-04-09 17:01:56.504762','2018-04-09 17:01:56.504805','手机','http://www.itcast.cn','','',1,1,6),(16,'2018-04-09 17:02:11.330329','2018-04-09 17:02:11.330373','配件','http://www.itcast.cn','','',2,1,6),(17,'2018-04-09 17:02:27.171626','2018-04-09 17:02:27.171669','充值','http://www.itcast.cn','','',3,1,6),(18,'2018-04-09 17:02:47.086939','2018-04-09 17:02:47.086983','优惠券','http://www.itcast.cn','','',4,1,6),(19,'2018-04-09 17:03:06.144946','2018-04-09 17:03:06.144990','荣耀手机','http://www.itcast.cn','','',1,1,7),(20,'2018-04-09 17:03:23.268285','2018-04-09 17:03:23.268333','国美手机','http://www.itcast.cn','','',2,1,7),(21,'2018-04-09 17:03:36.403398','2018-04-09 17:03:36.403463','华为手机','http://www.itcast.cn','','',3,1,7),(22,'2018-04-09 17:03:54.000395','2018-04-09 17:03:54.000460','热销推荐','http://www.itcast.cn','','',4,1,7),(23,'2018-04-09 17:04:12.517924','2018-04-09 17:04:12.517972','以旧换新','http://www.itcast.cn','','',5,1,7),(24,'2018-04-09 17:04:29.338056','2018-04-09 17:04:29.338132','潮3C','http://www.itcast.cn','','',6,1,7),(25,'2018-04-09 17:04:45.403852','2018-04-09 17:04:45.403917','全面屏','http://www.itcast.cn','','',7,1,7),(26,'2018-04-09 17:04:58.159270','2018-04-09 17:04:58.159321','守护宝','http://www.itcast.cn','','',8,1,7),(27,'2018-04-09 17:05:14.234438','2018-04-09 17:05:14.234482','存储卡','http://www.itcast.cn','','',9,1,7),(28,'2018-04-10 08:51:33.422870','2018-04-10 08:51:33.422915','360手机 N6 Pro 全网通','http://www.itcast.cn','group1/M00/00/01/CtM3BVrMexWAfodJAAAhg8MeEWU8364862','￥ 2699.00',1,1,8),(29,'2018-04-10 08:52:50.280197','2018-04-10 08:52:50.280243','iPhone X','http://www.itcast.cn','group1/M00/00/01/CtM3BVrMe2KAGXDKAAAVASh8SzY6938726','￥ 7788.00',2,1,8),(30,'2018-04-10 08:56:33.016220','2018-04-10 09:16:59.298002','荣耀 畅玩7A 全网通 极光蓝','http://www.itcast.cn','group1/M00/00/01/CtM3BVrMgQuAM4-sAABPvjDmrZE7647305','￥ 749.00',3,1,8),(31,'2018-04-10 08:57:52.744863','2018-04-10 09:18:36.211831','魅蓝 S6 全网通','http://www.itcast.cn','group1/M00/00/01/CtM3BVrMgWyAH_f1AAAQuFJkR2o1196559','￥1199.00',4,1,8),(32,'2018-04-10 08:59:19.379261','2018-04-10 09:20:59.490599','红米5Plus 全网通 浅蓝','http://www.itcast.cn','group1/M00/00/01/CtM3BVrMgX2AeXiGAABuWTn7Wr09762364','￥1299.00',5,1,8),(33,'2018-04-10 09:19:52.078636','2018-04-10 09:21:15.251997','OPPO A1 全网通 深海蓝','http://www.itcast.cn','group1/M00/00/01/CtM3BVrMgbiARBnzAABbhp78Lqs6191821','￥1399.00',6,1,8),(34,'2018-04-10 09:20:43.322594','2018-04-10 09:21:08.660170','华为 nova3e 全网通 幻夜黑','http://www.itcast.cn','group1/M00/00/01/CtM3BVrMgeuAYEocAABd3TzhhGw1571126','￥1999.00',7,1,8),(35,'2018-04-10 09:22:14.074590','2018-04-10 09:22:14.074656','OPPO R15 全网通 梦镜红','http://www.itcast.cn','group1/M00/00/01/CtM3BVrMgkaAWyHAAABbrVH9a7o5762009','￥3299.00',8,1,8),(36,'2018-04-10 09:22:52.988391','2018-04-10 09:22:52.988518','荣耀V10 全网通 标配版 沙滩金','http://www.itcast.cn','group1/M00/00/01/CtM3BVrMgmyAB_1AAABoaAzPPW86045138','￥2499.00',9,1,8),(37,'2018-04-10 09:23:26.963050','2018-04-10 09:23:26.963128','vivo X21 异形全面屏 全网通','http://www.itcast.cn','group1/M00/00/01/CtM3BVrMgo6Aa3OTAAA82h3PXzw9976088','￥3198.00',10,1,8),(38,'2018-04-10 09:29:30.877589','2018-04-10 09:29:30.877630','华为P10 全网通','http://www.itcast.cn','group1/M00/00/01/CtM3BVrMg_qACjBsAAActVXQUoc6433633','￥3488.00',1,1,10),(39,'2018-04-10 09:29:59.145437','2018-04-10 09:29:59.145821','小米 红米5 全网通版','http://www.itcast.cn','group1/M00/00/01/CtM3BVrMhBeAaZ9OAABuZHjPsV88472096','￥699.00',2,1,10),(40,'2018-04-10 09:30:29.868913','2018-04-10 09:30:29.868969','魅蓝 Note6 全网通公开版','http://www.itcast.cn','group1/M00/00/01/CtM3BVrMhDWAEwgEAABPce7je4w1228836','￥1499.00',3,1,10),(41,'2018-04-10 09:31:07.855868','2018-04-10 09:31:07.855915','红米5Plus 全网通','http://www.itcast.cn','group1/M00/00/01/CtM3BVrMhFuAB5eZAAAaQIF-UNs3707070','￥1299.00',4,1,10),(42,'2018-04-10 09:31:42.980397','2018-04-10 09:31:42.980445','荣耀9青春版 标配版','http://www.itcast.cn','group1/M00/00/01/CtM3BVrMhH6AAjD4AABS1vBu6x01229529','￥1099.00',5,1,10),(43,'2018-04-10 09:34:08.867671','2018-04-10 09:34:08.867712','华为 畅享8 全网通','http://www.itcast.cn','group1/M00/00/01/CtM3BVrMhRCAB5hsAAAQZye4aIM5257140','￥1299.00',6,1,10),(44,'2018-04-10 09:35:12.710916','2018-04-10 09:35:12.710989','荣耀 畅玩7X 尊享版','http://www.itcast.cn','group1/M00/00/01/CtM3BVrMhVCAFC8tAABonSNLGHA3584281','￥1799.00',7,1,10),(45,'2018-04-10 09:35:42.251919','2018-04-10 09:35:42.251963','华为 nova3e 全网通 幻夜黑','http://www.itcast.cn','group1/M00/00/01/CtM3BVrMhW6Ac7QMAABd3TzhhGw0583536','￥1999.00',8,1,10),(46,'2018-04-10 09:36:12.028644','2018-04-10 09:36:12.028685','魅族 RPO 7 Plus 全网通','http://www.itcast.cn','group1/M00/00/01/CtM3BVrMhYyAOjMVAABU1kCuf_48013827','￥2799.00',9,1,10),(47,'2018-04-10 09:36:36.804759','2018-04-10 09:36:36.804804','三星 S8 Plus 全网通','http://www.itcast.cn','group1/M00/00/01/CtM3BVrMhaSAK3QLAAA7LKRGwzQ0348867','￥5499.00',10,1,10),(48,'2018-04-10 09:38:59.226650','2018-04-10 09:38:59.226695','Aogress一体双用数据线DC-28金','http://www.itcast.cn','group1/M00/00/01/CtM3BVrMhjOAdMNbAAAR1JGA_cA5064317','￥29.00',1,1,11),(49,'2018-04-10 09:39:32.483523','2018-04-10 09:39:32.483585','黑客iPhone X 钢化膜','http://www.itcast.cn','group1/M00/00/01/CtM3BVrMhlSAP_27AAAW_YBdNEk8530912','￥29.00',2,1,11),(50,'2018-04-10 09:40:08.968290','2018-04-10 09:40:08.968367','黑客 3D曲面 全屏钢化膜','http://www.itcast.cn','group1/M00/00/01/CtM3BVrMhniADXZpAAALTWT-dfQ6160056','￥99.00',4,1,11),(51,'2018-04-10 09:40:40.405191','2018-04-10 09:40:40.405231','三星（SAMSUNG）存储卡 64G','http://www.itcast.cn','group1/M00/00/01/CtM3BVrMhpiAV3lJAABiLlkgy2Y9166507','￥169.00',5,1,11),(52,'2018-04-10 09:42:15.130337','2018-04-10 09:42:15.130419','浦诺菲(pivoful) PUC-15 Type-C 数据线','http://www.itcast.cn','group1/M00/00/01/CtM3BVrMhveAOh8EAAA1ykQ-kAU6900992','￥19.90',6,1,11),(53,'2018-04-10 09:43:07.486074','2018-04-10 09:43:07.486118','好格(Aogress) A-100E移动电源','http://www.itcast.cn','group1/M00/00/01/CtM3BVrMhyuAEf95AABFDj_owsg4241256','￥99.00',7,1,11),(54,'2018-04-10 09:43:38.901332','2018-04-10 09:43:38.901374','卡士奇 存储卡','http://www.itcast.cn','group1/M00/00/01/CtM3BVrMh0qAavITAABOVXYg3SI5232882','￥29.90',8,1,11),(55,'2018-04-10 09:44:39.359738','2018-04-10 09:44:39.359783','捷波朗(Jabra)OTE23 运动蓝牙耳机','http://www.itcast.cn','group1/M00/00/01/CtM3BVrMh4eAWdF2AAA-Fkkc5rM1921911','￥299.00',9,1,11),(56,'2018-04-10 09:45:17.804328','2018-04-10 09:45:17.804368','besiterBST-0109FO强尼思','http://www.itcast.cn','group1/M00/00/01/CtM3BVrMh62AUlDTAAA-SfqPszY5890026','￥99.00',10,1,11),(57,'2018-04-10 09:58:35.242596','2018-04-10 09:58:35.242654','小米九号平衡车','http://www.itcast.cn','group1/M00/00/01/CtM3BVrMisuAJnyWAABYJxXfN8w9822011','加100元送小米汽车',1,1,16),(58,'2018-04-10 09:59:16.706582','2018-04-10 09:59:16.706628','小米空气净化器2','http://www.itcast.cn','group1/M00/00/01/CtM3BVrMivSAUTWcAAANpJ-t9xg5938130','加价10元送滤芯',2,1,16),(59,'2018-04-11 06:39:11.953183','2018-04-11 06:39:11.953229','Apple Watch S3 GPS版','http://www.itcast.cn','group1/M00/00/01/CtM3BVrNrY-AdBacAAA7DYB8sjU0120233','加1元换够蓝牙耳机',3,1,16),(60,'2018-04-11 06:40:29.270078','2018-04-11 06:40:29.270123','裴讯智能体脂秤S7P','http://www.itcast.cn','group1/M00/00/01/CtM3BVrNrd2AbRH-AAALOATUqqM8030242','加1元换够南浮电池',4,1,16),(61,'2018-04-11 06:41:03.054344','2018-04-11 06:41:03.054390','360儿童手表电话SE2','http://www.itcast.cn','group1/M00/00/01/CtM3BVrNrf-AJ1ZjAAB_vAApFkw8201014','￥169.00',5,1,16),(62,'2018-04-11 06:42:11.402524','2018-04-11 06:42:11.402782','S2PGHW-521蓝牙耳机','http://www.itcast.cn','group1/M00/00/01/CtM3BVrNrkOAYXcbAABQocGJtes4517631','￥449.00',6,1,16),(63,'2018-04-11 06:42:47.985726','2018-04-11 06:42:47.985771','科大讯飞 翻译机','http://www.itcast.cn','group1/M00/00/01/CtM3BVrNrmeAPQkiAAAKCg08y3w4028142','加1元换够电池',7,1,16),(64,'2018-04-11 06:43:19.285413','2018-04-11 06:43:19.285477','Apple AirPods蓝牙耳机','http://www.itcast.cn','group1/M00/00/01/CtM3BVrNroeAUxHkAAAKhSBwnSk3723835','￥1288.00',8,1,16),(65,'2018-04-11 06:43:59.651504','2018-04-11 06:43:59.651581','ILIFE V5 智能扫地机器人','http://www.itcast.cn','group1/M00/00/01/CtM3BVrNrq-AbFajAABb8Hp05302964728','加1元换够充电器',9,1,16),(66,'2018-04-11 06:44:29.649982','2018-04-11 06:44:29.650036','360记录仪M301','http://www.itcast.cn','group1/M00/00/01/CtM3BVrNrs2AMHPbAABMxVYJeMo0602527','￥319.00',10,1,16),(67,'2018-04-11 06:46:32.465443','2018-04-11 06:46:32.465515','Apple iPad 平板电脑 2018款','http://www.itcast.cn','group1/M00/00/01/CtM3BVrNr0iAAbCEAABZEWPGxc48830214','￥2388.00',1,1,18),(68,'2018-04-11 06:47:11.689035','2018-04-11 06:47:11.689102','华硕飞行堡垒五代游戏本','http://www.itcast.cn','group1/M00/00/01/CtM3BVrNr2-AbNUxAABwpN-gR8E7784256','￥5999.00',2,1,18),(69,'2018-04-11 06:48:08.629095','2018-04-11 06:48:08.629138','ThinkPad T480','http://www.itcast.cn','group1/M00/00/01/CtM3BVrNr6iAWKHsAAAcWfJ6OD00441704','￥8399.00',3,1,18),(70,'2018-04-11 06:48:34.571822','2018-04-11 06:48:34.571868','华硕飞行堡垒五代游戏本','http://www.itcast.cn','group1/M00/00/01/CtM3BVrNr8KAD6b2AAByGLpNQV01684706','￥6299.00',4,1,18),(71,'2018-04-11 06:49:16.497815','2018-04-26 12:46:17.580482','艾比格特 无线移动WIFI','http://www.itcast.cn','group1/M00/00/02/CtM3BVrhyhmAehqbAAA3XtuXCto1322736','￥1399.00',5,1,18),(72,'2018-04-11 06:49:49.839309','2018-04-11 06:49:49.839349','360 巴迪龙儿童手表','http://www.itcast.cn','group1/M00/00/01/CtM3BVrNsA2AQUMbAAAbb_vBV6I1599925','￥999.00',6,1,18),(73,'2018-04-11 06:50:19.092920','2018-04-11 06:50:19.093006','Lenovo 星球大战 绝地挑战 AR眼镜','http://www.itcast.cn','group1/M00/00/01/CtM3BVrNsCuAUvllAAAOkY17G984349519','￥1999.00',7,1,18),(74,'2018-04-11 06:50:41.252312','2018-04-11 06:50:41.252453','HTC VR眼镜','http://www.itcast.cn','group1/M00/00/01/CtM3BVrNsEGAZTfyAAAasplERbc8856337','￥4299.00',8,1,18),(75,'2018-04-11 06:51:12.922333','2018-04-11 06:51:12.922378','Apple Watch S3 蜂窝版','http://www.itcast.cn','group1/M00/00/01/CtM3BVrNsGCAeDZeAABtIYY5-s41601603','￥3188.00',9,1,18),(76,'2018-04-11 06:51:40.271373','2018-04-11 06:51:40.271422','360电话手表 X1Pro','http://www.itcast.cn','group1/M00/00/01/CtM3BVrNsHyANXdyAABeDo_Qzeg1095047','￥1499.00',10,1,18),(77,'2018-04-11 06:53:31.774835','2018-04-11 06:53:31.774982','小米笔记本Air','http://www.itcast.cn','group1/M00/00/01/CtM3BVrNsOuAQbJYAABoachTxTo8223966','',1,1,13),(78,'2018-04-11 06:53:46.540973','2018-04-11 06:53:46.541041','电脑','http://www.itcast.cn','','',1,1,14),(79,'2018-04-11 06:54:00.356620','2018-04-11 06:54:00.356669','数码','http://www.itcast.cn','','',2,1,14),(80,'2018-04-11 06:54:11.361324','2018-04-11 06:54:11.361367','配件','http://www.itcast.cn','','',3,1,14),(81,'2018-04-11 06:54:21.777505','2018-04-11 06:54:21.777549','潮电子','http://www.itcast.cn','','',4,1,14),(82,'2018-04-11 06:54:36.170021','2018-04-11 06:54:36.170082','iPad新品','http://www.itcast.cn','','',1,1,15),(83,'2018-04-11 06:54:50.484452','2018-04-11 06:54:50.484499','限量购','http://www.itcast.cn','','',2,1,15),(84,'2018-04-11 06:55:11.333884','2018-04-11 06:55:11.333934','单反相机','http://www.itcast.cn','','',3,1,15),(85,'2018-04-11 06:55:31.975211','2018-04-11 06:55:31.975285','智能家具','http://www.itcast.cn','','',4,1,15),(86,'2018-04-11 06:55:43.070748','2018-04-11 06:55:43.070796','智能路由','http://www.itcast.cn','','',5,1,15),(87,'2018-04-11 06:55:57.563944','2018-04-11 06:55:57.563999','限时抢','http://www.itcast.cn','','',6,1,15),(88,'2018-04-11 06:56:14.604570','2018-04-11 06:56:14.604661','颂拓','http://www.itcast.cn','','',7,1,15),(89,'2018-04-11 06:56:25.639226','2018-04-11 06:56:25.639271','微单','http://www.itcast.cn','','',8,1,15),(90,'2018-04-11 06:56:34.836303','2018-04-11 06:56:34.836374','耳机','http://www.itcast.cn','','',9,1,15),(91,'2018-04-11 06:56:58.113652','2018-04-11 06:56:58.113703','水星家纺','http://www.itcast.cn','group1/M00/00/01/CtM3BVrNsbqAbi4CAABYmW4pmPA1782942','',1,1,21),(92,'2018-04-11 06:57:13.215501','2018-04-11 06:57:13.215548','家具日用','http://www.itcast.cn','','',1,1,22),(93,'2018-04-11 06:57:30.689560','2018-04-11 06:57:30.689647','家纺寝具','http://www.itcast.cn','','',2,1,22),(94,'2018-04-11 06:57:50.983438','2018-04-11 06:57:50.983481','住宅家具','http://www.itcast.cn','','',3,1,22),(95,'2018-04-11 06:58:03.324082','2018-04-11 06:58:03.324128','厨具餐饮','http://www.itcast.cn','','',1,1,23),(96,'2018-04-11 06:58:13.694750','2018-04-11 06:58:13.694795','被子','http://www.itcast.cn','','',2,1,23),(97,'2018-04-11 06:58:31.412903','2018-04-11 06:58:31.412949','实木床','http://www.itcast.cn','','',3,1,23),(98,'2018-04-11 06:58:52.598947','2018-04-11 06:58:52.598992','箭牌马桶','http://www.itcast.cn','','',4,1,23),(99,'2018-04-11 06:59:07.562439','2018-04-11 06:59:07.562541','指纹锁','http://www.itcast.cn','','',5,1,23),(100,'2018-04-11 06:59:24.628095','2018-04-11 06:59:24.628162','电饭煲','http://www.itcast.cn','','',6,1,23),(101,'2018-04-11 06:59:37.707050','2018-04-11 06:59:37.707098','热水器','http://www.itcast.cn','','',7,1,23),(102,'2018-04-11 06:59:48.635658','2018-04-11 06:59:48.635707','席梦思','http://www.itcast.cn','','',8,1,23),(103,'2018-04-11 06:59:57.465653','2018-04-11 06:59:57.465696','沙发','http://www.itcast.cn','','',9,1,23),(104,'2018-04-11 07:02:03.780376','2018-04-11 07:02:03.780419','洁柔纸巾','http://www.itcast.cn','group1/M00/00/01/CtM3BVrNsuuAQo25AAAmP_AGNMA9808303','￥45.90',1,1,24),(105,'2018-04-11 07:02:46.547111','2018-04-11 07:02:46.547187','花仙子除湿剂','http://www.itcast.cn','group1/M00/00/01/CtM3BVrNsxaAeU4HAAAkQDJCGSY6809195','￥19.90',2,1,24),(106,'2018-04-11 07:03:18.325791','2018-04-11 07:03:18.325869','超能洗衣液','http://www.itcast.cn','group1/M00/00/01/CtM3BVrNszaAMu2PAACwnbap8zI9797082','惊喜价',3,1,24),(107,'2018-04-11 07:04:04.509724','2018-04-11 07:04:04.509770','创简坊 扫帚','http://www.itcast.cn','group1/M00/00/01/CtM3BVrNs2SAf2DEAAAGl2-3v5k2172012','惊喜价',4,1,24),(108,'2018-04-11 07:04:34.799452','2018-04-11 07:04:34.799494','万象玻璃杯','http://www.itcast.cn','group1/M00/00/01/CtM3BVrNs4KAIlJKAAAQmKypd2c1901811','爆款热销',5,1,24),(109,'2018-04-11 07:05:10.845016','2018-04-11 07:05:10.845072','爱丽丝收纳箱','http://www.itcast.cn','group1/M00/00/01/CtM3BVrNs6aAea7bAAAIoddXpoA5854653','￥66.00',6,1,24),(110,'2018-04-11 07:05:41.147138','2018-04-11 07:05:41.147210','塑料袋 加厚','http://www.itcast.cn','group1/M00/00/01/CtM3BVrNs8WAZsplAAB-c4wo3kI9077289','跳楼价',7,1,24),(111,'2018-04-11 07:06:12.674584','2018-04-11 07:06:12.674634','特白惠 塑料杯','http://www.itcast.cn','group1/M00/00/02/CtM3BVrNs-SAaLqBAAAPB44z-fw7327519','实惠价',8,1,24),(112,'2018-04-11 07:06:54.675238','2018-04-11 07:06:54.675282','Bormioli Rocco意大利进口水果杯','http://www.itcast.cn','group1/M00/00/02/CtM3BVrNtA6AFtbDAAAVJIjSdl43078544','买一送一',9,1,24),(113,'2018-04-11 07:07:29.946108','2018-04-11 07:07:29.946151','宜兴紫砂壶','http://www.itcast.cn','group1/M00/00/02/CtM3BVrNtDGAdlzlAAAZZRjOIrQ5323041','￥220.00',10,1,24),(114,'2018-04-11 07:09:57.168028','2018-04-11 07:09:57.168075','苏泊尔 炒锅','http://www.itcast.cn','group1/M00/00/02/CtM3BVrNtMWANuqTAACac0TCaxU2674435','￥329.00 惠',1,1,25),(115,'2018-04-11 07:10:32.939492','2018-04-11 07:10:32.939538','双立人 多用双刀','http://www.itcast.cn','group1/M00/00/02/CtM3BVrNtOiAKex1AAAOZc14LLQ2319263','惊喜价',2,1,25),(116,'2018-04-11 07:11:13.792342','2018-04-11 07:11:13.792386','爱仕达高压锅','http://www.itcast.cn','group1/M00/00/02/CtM3BVrNtRGAGUbMAACY-WS_oQg9101415','特惠价',3,1,25),(117,'2018-04-11 07:12:01.447582','2018-04-11 07:12:01.447628','维艾圆形不秀钢盆','http://www.itcast.cn','group1/M00/00/02/CtM3BVrNtUGACPW-AAAWNwYc_Yg9317761','￥69.90',4,1,25),(118,'2018-04-11 07:12:34.001525','2018-04-11 07:12:34.001609','家栢利304不锈钢壁挂','http://www.itcast.cn','group1/M00/00/02/CtM3BVrNtWKAUKPkAADhQEAcAgQ4155172','￥198.00',5,1,25),(119,'2018-04-11 07:13:17.630873','2018-04-11 07:13:17.630916','生物海瓷','http://www.itcast.cn','group1/M00/00/02/CtM3BVrNtY2ABEOfAAAWaWuGKss3304555','震撼价',6,1,25),(120,'2018-04-11 07:13:45.655300','2018-04-11 07:13:45.655340','实木筷','http://www.itcast.cn','group1/M00/00/02/CtM3BVrNtamAdrqPAAAYsg3AvQ86108884','买二送一',7,1,25),(121,'2018-04-11 07:14:11.876255','2018-04-11 07:14:11.876328','菜板','http://www.itcast.cn','group1/M00/00/02/CtM3BVrNtcOAYTH1AABVIz70wKU1556174','只要￥149.00',8,1,25),(122,'2018-04-11 07:14:42.828364','2018-04-11 07:14:42.828410','刻度玻璃瓶','http://www.itcast.cn','group1/M00/00/02/CtM3BVrNteKAZhHCAAAMrIL-ugE2533088','白菜价',9,1,25),(123,'2018-04-11 07:15:11.019433','2018-04-11 07:15:11.019475','韩国进口 密封盒','http://www.itcast.cn','group1/M00/00/02/CtM3BVrNtf-AY0FGAAAZwGscZq42512400','￥39.00',10,1,25);
/*!40000 ALTER TABLE `tb_content` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-07-24 21:58:26
