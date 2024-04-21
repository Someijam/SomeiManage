# 数据库：学生成绩管理系统 someimanage

## 命名约定

请大致遵守如下约定

* CSS的class：`[page]-[compo]-[dataname]-(pos)` 如 `index-head-navbar-logo-top` 其中dataname可以嵌套“-”
* script内的常量以及变量：`[page]_[compo]_[data]` 如 `student_table_contents`
* script内的函数名：`[page]_[compo]_[func]()` 如 `score_drawer_newsc_show()`

## 初始化项目
```shell
npm install
npm run serve
npm run build
npm run lint
```

### 自定义设置
参照 [Configuration Reference](https://cli.vuejs.org/config/).