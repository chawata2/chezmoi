# dotfiles (chezmoi)

個人のdotfilesをchezmoiで管理するリポジトリ。

参考: https://www.chezmoi.io/

---

## インストール

```sh
brew install chezmoi
```

---

## dotfilesを適用する

```sh
chezmoi init git@github.com:chawata2/chezmoi.git
chezmoi apply
```

---

## 日常の使い方

### ファイルを追加する

```sh
chezmoi add ~/.zshrc
```

### ファイルを編集する

```sh
chezmoi edit ~/.zshrc
```

編集後に適用する:

```sh
chezmoi apply
```

### 配置先を直接編集してしまった場合

`chezmoi edit` を使わず配置先（例: `~/.zshrc`）を直接編集してしまったとき、変更をchezmoiのソースに反映するには `re-add` を使う。

```sh
# 特定ファイルを再同期
chezmoi re-add ~/.zshrc

# 管理対象ファイルをすべて再同期
chezmoi re-add
```

---

## 差分の確認

ソースと配置先の差分を確認する:

```sh
chezmoi diff
```

リモートの変更と現在の状態の差分を確認する:

```sh
chezmoi git -- fetch
chezmoi git -- diff HEAD origin/master
```

---

## アップデート（リモートの変更を取り込む）

リモートリポジトリの最新変更を pull して apply まで一括実行する:

```sh
chezmoi update
```

pull のみ行う場合:

```sh
chezmoi git -- pull
chezmoi apply
```

---

## リモートへの同期（コミット & プッシュ）

```sh
chezmoi diff
chezmoi git -- commit -m "Update"
chezmoi git -- push
```

---

## 管理対象ファイルの確認

```sh
# 管理しているファイルの一覧
chezmoi managed

# ソースディレクトリを開く
chezmoi cd
```

---

## 参考

- [chezmoi 公式ドキュメント](https://www.chezmoi.io/)
- [chezmoi を使ったdotfiles管理](https://zenn.dev/ryo_kawamata/articles/introduce-chezmoi)
