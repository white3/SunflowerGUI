CREATE TABLE HAOffsetTabel(
    id INTEGER PRIMARY KEY AUTOINCREMENT,  // 定义唯一id
    ha FLOAT NOT NULL,                                // 时角
    haOffset FLOAT NOT NULL,                         // 赤纬改正量
    localTime DATETIME NOT NULL,                    // 时间
    version INT NOT NULL,                           // 改修正值的版本
    target char(50)                                 // 观测目标
);
CREATE TABLE DECOffsetTabel(
    id INTEGER PRIMARY KEY AUTOINCREMENT,           // 定义唯一id
    dec FLOAT NOT NULL,                               // 赤纬
    decOffset FLOAT NOT NULL,                        // 赤纬改正量
    localTime DATETIME NOT NULL,                    // 时间
    version INT NOT NULL,                           // 改修正值的版本
    target char(50)                                 // 观测目标
);