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

## Github GitLab共存

### 生成Github SSH

```
ssh-keygen -t rsa -C "XXXXX@gmail.com"
取名为id_github_ras
ssh-add ~/.ssh/id_github_rsa
```

### 生成GitLab SSH

```
ssh-keygen -t rsa -C "XXXXX@gmail.com"
取名为id_gitlab_ras
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
