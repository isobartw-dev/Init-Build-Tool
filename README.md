InitBuildTool sublime text package
=======================================
sublime text 自動化流程開發環境，將自動化任務及功能加入開發專案 [自動化流程 step by step](https://hackmd.io/s/S1ohqCzN)
- task (自動化任務檔案)
- package.json (自動化需要使用的 package 及 npm script)
- build system (sublime project build system)

## 安裝
1. Ctrl+ Shift + p > Add Repository > 貼上 https://<i></i>github.com/isobartw-dev/InitBuildTool
2. Ctrl+ Shift + p > Install Package > InitBuildTool
3. clone [CampaignBuildTool](https://github.com/isobartw-dev/CampaignBuildTool) 專案到電腦

## 設定
Preferences > Package Setting > InitBuildTool > Settings – User  
設定 CampaignBuildTool 的路徑
```
{
    "workflowPackagePath":"D:/XXX/XXX..."
}
```
## 使用
- ``Ctrl+ Shift + p`` > 建立自動化流程：Campaign
- ``Alt + Shift + i``

## 更新
當 CampaignBuildTool 更新時，執行 InitBuildTool 即可更新為最新版本
