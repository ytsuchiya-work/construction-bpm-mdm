# 建設BPM+MDM

建設業向けのマスタデータ管理（MDM）と工程管理（BPM）を統合したWebアプリケーション。
3階層のマスタデータ構造とAIによるテーブル分析・統合機能、ReactFlowによるビジュアル工程管理を提供する。

## 技術スタック

### バックエンド

| パッケージ | バージョン | 用途 |
|-----------|-----------|------|
| FastAPI | 0.115.0 | APIサーバー |
| Uvicorn | 0.30.6 | ASGIサーバー |
| SQLAlchemy | 2.0.35 | ORM |
| Pydantic | 2.9.2 | バリデーション |
| aiofiles | 24.1.0 | 非同期ファイルI/O |

### フロントエンド

| パッケージ | バージョン | 用途 |
|-----------|-----------|------|
| React | 18.3.1 | UIフレームワーク |
| React Router | 6.26.2 | ルーティング |
| ReactFlow | 11.11.4 | フローダイアグラム |
| Lucide React | 0.447.0 | アイコン |
| Vite | 5.4.9 | ビルドツール |
| TailwindCSS | 3.4.13 | CSSフレームワーク |

### インフラ

| 項目 | 内容 |
|------|------|
| データベース | SQLite |
| デプロイ先 | Databricks Apps |
| ホスティング | FastAPIによるSPA配信 + APIサーバー一体型 |

## システムアーキテクチャ

```
┌─────────────────────────────────────────────────────┐
│                   Databricks Apps                    │
│                                                     │
│  ┌───────────────────────────────────────────────┐  │
│  │              Uvicorn (port 8000)               │  │
│  │  ┌─────────────────────────────────────────┐  │  │
│  │  │              FastAPI                     │  │  │
│  │  │                                         │  │  │
│  │  │  /api/*  ──→  APIエンドポイント群       │  │  │
│  │  │  /assets/* ──→ 静的ファイル配信         │  │  │
│  │  │  /*       ──→ SPA (index.html)          │  │  │
│  │  │                                         │  │  │
│  │  │  ┌─────────────┐  ┌──────────────────┐  │  │  │
│  │  │  │ SQLAlchemy   │  │ AI Analysis     │  │  │  │
│  │  │  │   ORM        │  │  Engine         │  │  │  │
│  │  │  └──────┬───────┘  └──────────────────┘  │  │  │
│  │  │         │                                │  │  │
│  │  │  ┌──────▼───────┐                        │  │  │
│  │  │  │   SQLite DB   │                        │  │  │
│  │  │  └──────────────┘                        │  │  │
│  │  └─────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                   ブラウザ                            │
│  ┌─────────────────────────────────────────────────┐│
│  │  React SPA (Vite ビルド)                        ││
│  │  ┌──────────┐ ┌──────────────┐ ┌────────────┐  ││
│  │  │Dashboard │ │ MasterData   │ │   BPM      │  ││
│  │  │  Page    │ │   Page       │ │   Page     │  ││
│  │  └──────────┘ └──────────────┘ └────────────┘  ││
│  └─────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────┘
```

### ディレクトリ構成

```
construction-bpm-mdm/
├── backend/
│   ├── __init__.py
│   ├── main.py            # FastAPIアプリ & 全APIエンドポイント
│   ├── models.py           # SQLAlchemy ORMモデル
│   ├── schemas.py          # Pydanticスキーマ
│   ├── database.py         # DB接続設定
│   ├── ai_analysis.py      # AI分析エンジン
│   └── seed.py             # 初期データ投入
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # ルーティング & ナビゲーション
│   │   ├── main.jsx        # エントリポイント
│   │   ├── index.css       # グローバルCSS
│   │   └── pages/
│   │       ├── DashboardPage.jsx    # ダッシュボード
│   │       ├── MasterDataPage.jsx   # マスタデータ管理
│   │       └── BPMPage.jsx          # 工程管理
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── index.html
├── static/                 # Viteビルド出力（デプロイ用）
│   ├── index.html
│   └── assets/
├── app.yaml                # Databricks Appsデプロイ設定
├── requirements.txt        # Python依存パッケージ
├── .gitignore
└── .databricksignore       # Databricks sync除外設定
```

## ER図

```
┌──────────────────────┐
│      LayerNode       │
│──────────────────────│
│ id (PK)              │
│ name                 │         ┌─────────────────────────┐
│ description          │         │      MasterTable        │
│ layer_level          │         │─────────────────────────│
│ parent_id (FK:self)  │────1:N──│ id (PK)                 │
│ created_at           │         │ layer_node_id (FK)      │
│ updated_at           │         │ name                    │
└──────┬───────────────┘         │ description             │
       │                         │ record_count            │
       │ self                    │ created_at              │
       │ 1:N                     │ updated_at              │
       └─── LayerNode            └──────┬──────────┬───────┘
             (children)                 │          │
                                        │ 1:N      │ 1:N
                                        ▼          ▼
                            ┌──────────────────┐  ┌─────────────────┐
                            │  MasterColumn    │  │  MasterRecord   │
                            │──────────────────│  │─────────────────│
                            │ id (PK)          │  │ id (PK)         │
                            │ master_table_id  │  │ master_table_id │
                            │ name             │  │ record_index    │
                            │ column_type      │  │ data (JSON)     │
                            │ description      │  │ created_at      │
                            │ is_required      │  └─────────────────┘
                            │ source_object    │
                            │ source_field     │
                            │ sample_values    │
                            │ display_order    │
                            │ created_at       │
                            │ updated_at       │
                            └────────┬─────────┘
                                     │
                                     │ M:N
                                     │ (node_master_columns)
                                     │
┌──────────────────────┐             │
│       Project        │             │
│──────────────────────│             │
│ id (PK)              │             │
│ name                 │             │
│ description          │             │
│ status               │             │
│ created_by           │             │
│ created_at           │         ┌───▼────────────────┐
│ updated_at           │────1:N──│    ProcessNode     │
└──────────┬───────────┘         │────────────────────│
           │                     │ id (PK)            │
           │                     │ project_id (FK)    │
           │                     │ label              │
           │                     │ node_type          │
           │                     │ position_x         │
           │                     │ position_y         │
           │                     │ duration_days      │
           │                     │ status             │
           │                     │ description        │
           │                     │ created_at         │
           │                     │ updated_at         │
           │                     └────────────────────┘
           │                              ▲       ▲
           │                              │       │
           │                     source_node_id  target_node_id
           │                              │       │
           │     ┌────────────────────────┴───────┘
           │     │
           │ 1:N │
           │     ▼
           │  ┌──────────────────────┐
           └──│    ProcessEdge       │
              │──────────────────────│
              │ id (PK)              │
              │ project_id (FK)      │
              │ source_node_id (FK)  │
              │ target_node_id (FK)  │
              │ label                │
              │ created_at           │
              └──────────────────────┘
```

### モデル間の関係

| 関係 | 説明 |
|------|------|
| LayerNode → LayerNode | 自己参照 (parent_id)。3階層のツリー構造 |
| LayerNode → MasterTable | 1:N。各レイヤーに複数のマスタテーブル |
| MasterTable → MasterColumn | 1:N。テーブル内のカラム定義 |
| MasterTable → MasterRecord | 1:N。JSONデータとして格納されるレコード |
| Project → ProcessNode | 1:N。プロジェクト内の工程ノード |
| Project → ProcessEdge | 1:N。ノード間の接続 |
| ProcessNode ↔ MasterColumn | M:N。工程とマスタカラムの紐付け |

## デプロイ方法

### 前提条件

- Python 3.10+
- Node.js 18+
- Databricks CLI（認証設定済み）

### 1. ローカル環境セットアップ

```bash
# リポジトリのクローン
git clone https://github.com/ytsuchiya-work/construction-bpm-mdm.git
cd construction-bpm-mdm

# Python仮想環境 & 依存パッケージ
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# フロントエンド依存パッケージ
cd frontend
npm install
cd ..
```

### 2. ローカル開発サーバー起動

```bash
# バックエンド（ターミナル1）
source .venv/bin/activate
uvicorn backend.main:app --reload --port 8000

# フロントエンド（ターミナル2）
cd frontend
npm run dev
```

- フロントエンド開発サーバー: http://localhost:5173
- APIサーバー: http://localhost:8000
- Viteの設定により `/api` リクエストはバックエンドに自動プロキシされる

### 3. Databricks Appsへのデプロイ

```bash
# フロントエンドビルド（static/ ディレクトリに出力）
cd frontend
npm run build
cd ..

# Databricks Appsの作成（初回のみ）
databricks apps create construction-bpm-mdm \
  --description "建設BPM+MDM: マスタデータ管理 & 工程管理"

# ファイルをWorkspaceに同期
databricks sync . /Workspace/Users/<your-email>/construction-bpm-mdm --watch=false

# デプロイ
databricks apps deploy construction-bpm-mdm \
  --source-code-path /Workspace/Users/<your-email>/construction-bpm-mdm
```

### 4. デプロイ後の確認

デプロイが完了すると、以下のURLでアクセス可能になる:

```
https://construction-bpm-mdm-<workspace-id>.aws.databricksapps.com
```

ステータス確認:

```bash
databricks apps get construction-bpm-mdm
```

### 補足: .databricksignore

`databricks sync` 時に不要なファイル（`node_modules/`、フロントエンドソース等）を除外するため、`.databricksignore` ファイルを設定している。デプロイ対象は以下のみ:

- `backend/` — Pythonバックエンドコード
- `static/` — ビルド済みフロントエンド
- `app.yaml` — デプロイ設定
- `requirements.txt` — Python依存定義

## アプリの使用方法

### ダッシュボード (`/`)

アプリ全体の統計情報を表示する。レイヤー別のノード数、マスタテーブル数、カラム数、レコード数、プロジェクト数を一覧で確認できる。

### マスタデータ管理 (`/master`)

#### ツリーナビゲーション（左パネル）

- 3階層のレイヤー構造をツリー形式で表示
  - **レイヤー1**（青）: 全社共通基幹システム
  - **レイヤー2**（オレンジ）: 部門共通マスタ
  - **レイヤー3**（赤）: 現場別マスタ
- 各レイヤーの展開/折りたたみが可能
- レイヤー配下のマスタテーブルを一覧表示
- 検索ボックスでレイヤー名・テーブル名をフィルタリング

#### テーブル閲覧（メインエリア）

- テーブルをクリックすると詳細を表示
- **データ一覧タブ**: レコードをピボット形式（行=カラム、列=データ）で表示
- **カラム定義タブ**: カラム名・型・必須フラグ・ソース情報を表示。インライン編集に対応

#### AI分析（右パネル）

1. ツリーのチェックボックスで2つ以上のテーブルを選択
2. 「AI分析実行」ボタンをクリック
3. 4つのタブで分析結果を確認:
   - **列マッピング**: テーブル間のカラム対応関係と一致度
   - **レコード照合**: テーブル間のレコード一致度とマージプレビュー
   - **表記揺れ**: カタカナ表記・漢字同義語の検出
   - **統合サジェスト**: テーブル統合の提案と優先度
4. 「統合マスタ作成」でAIが分析結果に基づき統合テーブルを自動生成

#### テーブルの追加・削除

- レイヤーノード横の「＋」ボタンから新規テーブルを作成
- テーブル横のゴミ箱アイコンで削除（確認ダイアログ付き）
- 複数テーブルを選択して一括削除も可能

### 工程管理 (`/bpm`)

#### プロジェクト選択（左パネル上部）

- ドロップダウンから管理対象のプロジェクトを選択

#### フローキャンバス（メインエリア）

- ノードをドラッグで配置を変更
- ノード間をドラッグして接続（エッジ作成）
- ミニマップとズームコントロールで全体把握
- ステータスに応じた色分け:
  - グレー: 未着手
  - 青: 施工中
  - 緑: 完了

#### ノードの追加・編集（左パネル）

- パレットから「タスク」「マイルストーン」をキャンバスにドラッグ&ドロップで追加
- ノードをクリックすると左パネルに詳細を表示:
  - 名前、工期（日数）、ステータスを編集
  - マスタカラムとの紐付け（ツリーからチェックボックスで選択）
  - ノード削除
- エッジをクリックすると接続情報を表示・削除可能
