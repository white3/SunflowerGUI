CREATE TABLE HAOffsetTabel
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT, /* 定义唯一id */
    ha          FLOAT    NOT NULL,                 /* 时角 */
    haOffset    FLOAT    NOT NULL,                 /* 赤纬改正量 */
    globalClock DATETIME NOT NULL,                 /* 全局时钟, */
    version     INT      NOT NULL,                 /* 改修正值的版本 */
    target      char(200)                          /* 观测目标对象的json object */
);
CREATE TABLE DECOffsetTabel
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT, /* 定义唯一id */
    dec         FLOAT    NOT NULL,                 /* 赤纬 */
    decOffset   FLOAT    NOT NULL,                 /* 赤纬改正量 */
    globalClock DATETIME NOT NULL,                 /* 全局时钟的json object, 主要用于区别误差版本, 如果版本相同误差值不同,则通过全局时钟 */
    version     INT      NOT NULL,                 /* 改修正值的版本, 主要用于区别误差版本 */
    target      char(200)                          /* 观测目标的json object */
);