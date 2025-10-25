# 🧭 SEth Git 工作流程指南（Mac / SSH 版）(chatgpt 生成)

**仓库路径：**  
`/Users/liumengyao/Documents/GitHub/SEth`

本指南说明：当你修改完代码后，如何正确地更新并上传到 GitHub 仓库  
👉 `git@github.com:KULeuvenNESLFradio/SEth.git`

---

## ⚙️ 1. 基本准备

进入项目目录：
```bash
cd /Users/liumengyao/Documents/GitHub/SEth
```

查看当前分支：
```bash
git branch
```

如果不在主分支，可切换：
```bash
git switch main
```

---

## 🔄 2. 更新远端最新代码

在提交前，先同步远端仓库，避免冲突：
```bash
git fetch origin
git pull --rebase origin main
```
---

## ✍️ 3. 检查并暂存修改

查看已修改的文件：
```bash
git status
```

将所有变更添加到暂存区：
```bash
git add .
```

或只添加特定文件：
```bash
git add SEth_ArduinoDue_code/
```

---

## 💬 4. 提交修改

编写简短有意义的提交说明：
```bash
git commit -m "fix: adjust timing in Arduino Due receiver"
```

### 常见提交类型

| 类型 | 说明 |
|------|------|
| feat | 新功能 |
| fix | 修复问题 |
| refactor | 重构代码，不影响功能 |
| chore | 构建、配置或杂项改动 |
| docs | 文档更新 |
| test | 测试代码更新 |

---

## 🚀 5. 推送到 GitHub

推送本地更新到远端仓库：
```bash
git push origin main
```

如果是新建分支（第一次推送）：
```bash
git push -u origin my-branch-name
```

---

## ⚔️ 6. 常见问题与解决

### 🔑 提示输入用户名/密码

说明仍在使用 HTTPS。  
切换为 SSH：
```bash
git remote set-url origin git@github.com:KULeuvenNESLFradio/SEth.git
```

---

### 🚫 Permission denied (publickey)

1. 检查公钥是否添加到 GitHub：  
   [https://github.com/settings/keys](https://github.com/settings/keys)
2. 如果仓库属于组织（`KULeuvenNESLFradio`），确认已点击 **Enable SSO** 授权。
3. 确认本机已加载私钥：
   ```bash
   eval "$(ssh-agent -s)"
   ssh-add --apple-use-keychain ~/.ssh/id_ed25519
   ```

---

### 🌀 推送被拒（远端有更新）

```bash
git pull --rebase origin main
# 若有冲突，解决冲突后：
git add <文件名>
git rebase --continue
git push origin main
```

---

## 🧹 7. 忽略不必要文件

推荐 `.gitignore` 内容：
```
# macOS
.DS_Store

# VS Code
.vscode/

# Build / Temp
build/
out/
*.log
```

提交更新：
```bash
git add .gitignore
git commit -m "chore: update .gitignore"
git push
```

---

## ⚡️ 8. 一键同步脚本（可选）

如果你经常更新代码，可创建脚本 `sync.sh`：

```bash
#!/bin/bash
git add .
git commit -m "${1:-update}"
git pull --rebase origin main
git push origin main
```

给执行权限：
```bash
chmod +x sync.sh
```

使用方式：
```bash
./sync.sh "update receiver timing"
```

---

## ✅ 9. 快速总结（最常用上传流程）

```bash
cd /Users/liumengyao/Documents/GitHub/SEth
git status
git add .
git commit -m "说明修改"
git pull --rebase origin main
git push origin main
```

---

**Author:** Mengyao Liu  
**Last Updated:** 2025-10-25
