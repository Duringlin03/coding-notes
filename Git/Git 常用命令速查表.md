### 一、日常开发基础（最常用）
1. `git status` - 查看当前文件修改状态
2. `git add .` - 添加所有修改文件到暂存区
3. `git commit -m "备注信息"` - 提交暂存区文件到本地仓库
4. `git pull origin 分支名` - 拉取远程分支最新代码（避免冲突）
5. `git push origin 分支名` - 推送本地分支代码到远程

---

### 二、分支管理（开发/修复场景）
1. `git branch` - 查看本地所有分支
2. `git checkout -b 新分支名` - 新建并切换到新分支
3. `git checkout 已有分支名` - 切换到已存在的分支
4. `git merge 目标分支名` - 将目标分支代码合并到当前分支
5. `git branch -d 分支名` - 删除已合并的本地分支（安全删除）

---

### 三、错误回退与修改（补救场景）
1. `git checkout -- 文件名` - 撤销单个文件的未提交修改
2. `git reset --hard HEAD` - 撤销所有未提交修改（谨慎使用）
3. `git commit --amend -m "新备注"` - 修正上一次的提交信息
4. `git stash` - 暂存当前修改（临时切换分支用）
5. `git stash apply` - 应用最近一次的暂存内容

---

### 四、远程仓库操作（关联/同步场景）
1. `git clone 远程仓库地址` - 克隆远程仓库到本地
2. `git remote add origin 远程地址` - 关联本地仓库到远程
3. `git fetch` - 获取远程所有分支更新（不合并）
4. `git push --tags` - 推送本地标签到远程
5. `git log` - 查看提交历史（排查问题用）
