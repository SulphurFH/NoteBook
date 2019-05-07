# Git

## 项目上线

```
gco master
git pull
gco -b release-date
修改相关配置
git merge origin/dev
gst 
# 查看状态，如果前端项目需要注意dist目录，此目录为gulp生成的
git reset dist
git checkout dist
rm -rf dist/static/css/ak-mada-8d299507fc.min.css
rm -rf dist/static/js/ak-mada-d95eb6acc1.min.js
# 查看gst
git add .
git commit -m ''
git push origin release-date
GitLab发起合并申请，注意合并到master分支
```

## 解决冲突

```
git rebase origin/dev
gst
解决冲突
git add .
gst 查看是否还有冲突
有冲突---- git rebase --continue
无冲突---- git rebase --skip
git push origin XXXX -f
```

## 查看修改记录

```
git blame filename
```

## 撤销修改

```
git checkout . && git clean -xdf
```

## 彻底恢复到某个版本

```
git reset --hard 版本号的sha1
```

## Github GitLab共存

### 生成Github SSH

```
ssh-keygen -t rsa -C "XXXXX@gmail.com"
取名为id_github_rsa
ssh-add ~/.ssh/id_github_rsa
```

### 生成GitLab SSH

```
ssh-keygen -t rsa -C "XXXXX@gmail.com"
取名为id_gitlab_rsa
ssh-add ~/.ssh/id_gitlab_rsa
```

### ssh config

```
cd ~/.ssh
touch config

内容为

# gitlab
Host gitlab
  HostName gitlab.com
  PreferredAuthentications publickey
  IdentityFile ~/.ssh/id_gitlab_rsa

# github
Host github
  HostName github.com
  PreferredAuthentications publickey
  IdentityFile ~/.ssh/id_github_rsa
```

### 依次在Github与GitLab上添加SSH

### 测试

```
ssh -T git@gitlab.com
ssh -T git@github.com
```

### 其他

```
每个项目单独设置email与username
git config --global --unset user.name 取消全局设置
git config --global --unset user.email 取消全局设置

cd $(你的项目路径)
git config --local user.name
git config --local user.email
```

## GitFlow工作流  

```
git checkout -t origin/develop
git flow init -d
git checkout develop
git flow feature start fh-ft-xxxx
git flow feature finish
git flow feature rebase develop
git checkout release
git flow bugfix start fh-fix-xxxx
git flow bugfix finish --no-ff
git flow hotfix start fh-hotfix-xxxx
git flow hotfix finish
```

## 分支

```
# 列出所有本地分支
$ git branch

# 列出所有远程分支
$ git branch -r

# 列出所有本地分支和远程分支
$ git branch -a

# 新建一个分支，但依然停留在当前分支
$ git branch [branch-name]

# 新建一个分支，并切换到该分支
$ git checkout -b [branch]

# 新建一个分支，指向指定commit
$ git branch [branch] [commit]

# 新建一个分支，与指定的远程分支建立追踪关系
$ git branch --track [branch] [remote-branch]

# 切换到指定分支，并更新工作区
$ git checkout [branch-name]

# 切换到上一个分支
$ git checkout -

# 建立追踪关系，在现有分支与指定的远程分支之间
$ git branch --set-upstream [branch] [remote-branch]

# 合并指定分支到当前分支
$ git merge [branch]

# 选择一个commit，合并进当前分支
$ git cherry-pick [commit]

# 删除分支
$ git branch -d [branch-name]

# 删除远程分支
$ git push origin --delete [branch-name]
$ git branch -dr [remote/branch]
```