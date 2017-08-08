/**********************************/
/* Table Name: role */
/**********************************/
CREATE TABLE role(
		roleid                        		INT(10)		 NOT NULL AUTO_INCREMENT COMMENT 'roleid',
		rolename                      		VARCHAR(32)		 NOT NULL COMMENT 'rolename',
		ability                       		VARCHAR(32)		 NULL  COMMENT 'ability',
		createdate                    		DATE		 NOT NULL COMMENT 'createdate',
		updatedate                    		DATE		 NOT NULL COMMENT 'updatedate',
		deleteflag                    		CHAR(1)		 NOT NULL COMMENT 'deleteflag'
) COMMENT='role';

/**********************************/
/* Table Name: useInfo */
/**********************************/
CREATE TABLE useInfo(
		uid                           		INT(10)		 NOT NULL AUTO_INCREMENT COMMENT 'uid',
		username                      		VARCHAR(32)		 NULL  COMMENT 'username',
		mailaddress                   		VARCHAR(64)		 NOT NULL COMMENT 'mailaddress',
		password                      		VARCHAR(32)		 NOT NULL COMMENT 'password',
		roleid                        		INT(10)		 NULL  COMMENT 'roleid',
		createdate                    		DATE		 NOT NULL COMMENT 'createdate',
		updatedate                    		MEDIUMINT(10)		 NOT NULL COMMENT 'updatedate',
		deleteflag                    		CHAR(1)		 NOT NULL COMMENT 'deleteflag'
) COMMENT='useInfo';

/**********************************/
/* Table Name: projectInfo */
/**********************************/
CREATE TABLE projectInfo(
		projectname                   		VARCHAR(32)		 NOT NULL COMMENT 'projectname',
		appid                         		VARCHAR(64)		 NOT NULL COMMENT 'appid',
		secret                        		MEDIUMINT(10)		 NULL  COMMENT 'secret',
		createdate                    		DATE		 NOT NULL COMMENT 'createdate',
		updatedate                    		DATE		 NOT NULL COMMENT 'updatedate',
		deleteflag                    		CHAR(1)		 DEFAULT 0		 NOT NULL COMMENT 'deleteflag',
		uid                           		INT(10)		 NULL  COMMENT 'uid'
) COMMENT='projectInfo';

/**********************************/
/* Table Name: Table4 */
/**********************************/
CREATE TABLE TABLE_4(
		userlistid                    		INT(10)		 NOT NULL AUTO_INCREMENT COMMENT 'userlistid',
		uid                           		INT(10)		 NULL  COMMENT 'uid',
		appid                         		VARCHAR(64)		 NULL  COMMENT 'appid',
		createdate                    		DATE		 NOT NULL COMMENT 'createdate',
		updatedate                    		DATE		 NOT NULL COMMENT 'updatedate',
		deleteflag                    		CHAR(1)		 NOT NULL COMMENT 'deleteflag'
) COMMENT='Table4';

/**********************************/
/* Table Name: menuType */
/**********************************/
CREATE TABLE menuType(
		menutypeid                    		INTEGER(10)		 NOT NULL AUTO_INCREMENT COMMENT 'menutypeid',
		type                          		MEDIUMINT(10)		 NOT NULL COMMENT 'type'
) COMMENT='menuType';

/**********************************/
/* Table Name: menuList */
/**********************************/
CREATE TABLE menuList(
		menuid                        		INTEGER(10)		 NOT NULL AUTO_INCREMENT COMMENT 'menuid',
		menuname                      		VARCHAR(16)		 NOT NULL COMMENT 'menuname',
		parent                        		VARCHAR(16)		 NULL  COMMENT 'parent',
		key                           		VARCHAR(64)		 NULL  COMMENT 'key',
		url                           		VARCHAR(64)		 NULL  COMMENT 'url',
		menutypeid                    		INTEGER(10)		 NULL  COMMENT 'menutypeid'
) COMMENT='menuList';

/**********************************/
/* Table Name: ArticleColumnInfo */
/**********************************/
CREATE TABLE ArticleColumnInfo(
		articlecolid                  		INT(10)		 NOT NULL AUTO_INCREMENT COMMENT 'articlecolid',
		column                        		VARCHAR(32)		 NOT NULL COMMENT 'column',
		articleid                     		INT(10)		 NULL  COMMENT 'articleid'
) COMMENT='ArticleColumnInfo';

/**********************************/
/* Table Name: articleList */
/**********************************/
CREATE TABLE articleList(
		articleid                     		INT(10)		 NOT NULL AUTO_INCREMENT COMMENT 'articleid',
		title                         		MEDIUMINT(10)		 NOT NULL COMMENT 'title',
		dispseq                       		INT(10)		 NOT NULL COMMENT 'dispseq',
		author                        		VARCHAR(32)		 NULL  COMMENT 'author',
		uploadby                      		MEDIUMINT(10)		 NULL  COMMENT 'uploadby',
		createdate                    		DATE		 NOT NULL COMMENT 'createdate',
		updatedate                    		DATE		 NOT NULL COMMENT 'updatedate',
		deleteflag                    		CHAR(1)		 NOT NULL COMMENT 'deleteflag',
		articlecolid                  		INT(10)		 NULL  COMMENT 'articlecolid'
) COMMENT='articleList';


ALTER TABLE role ADD CONSTRAINT IDX_role_PK PRIMARY KEY (roleid);

ALTER TABLE useInfo ADD CONSTRAINT IDX_useInfo_PK PRIMARY KEY (uid);
ALTER TABLE useInfo ADD CONSTRAINT IDX_useInfo_FK0 FOREIGN KEY (roleid) REFERENCES role (roleid);

ALTER TABLE projectInfo ADD CONSTRAINT IDX_projectInfo_PK PRIMARY KEY (appid);
ALTER TABLE projectInfo ADD CONSTRAINT IDX_projectInfo_FK0 FOREIGN KEY (uid) REFERENCES useInfo (uid);

ALTER TABLE TABLE_4 ADD CONSTRAINT IDX_TABLE_4_PK PRIMARY KEY (userlistid);
ALTER TABLE TABLE_4 ADD CONSTRAINT IDX_TABLE_4_FK0 FOREIGN KEY (uid) REFERENCES useInfo (uid);
ALTER TABLE TABLE_4 ADD CONSTRAINT IDX_TABLE_4_FK1 FOREIGN KEY (appid) REFERENCES projectInfo (appid);

ALTER TABLE menuType ADD CONSTRAINT IDX_menuType_PK PRIMARY KEY (menutypeid);

ALTER TABLE menuList ADD CONSTRAINT IDX_menuList_PK PRIMARY KEY (menuid);
ALTER TABLE menuList ADD CONSTRAINT IDX_menuList_FK0 FOREIGN KEY (menutypeid) REFERENCES menuType (menutypeid);

ALTER TABLE ArticleColumnInfo ADD CONSTRAINT IDX_ArticleColumnInfo_PK PRIMARY KEY (articlecolid);

ALTER TABLE articleList ADD CONSTRAINT IDX_articleList_PK PRIMARY KEY (articleid);
ALTER TABLE articleList ADD CONSTRAINT IDX_articleList_FK0 FOREIGN KEY (articlecolid) REFERENCES ArticleColumnInfo (articlecolid);

