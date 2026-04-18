import json
from backend.models import LayerNode, MasterTable, MasterColumn, MasterRecord, Project, ProcessNode, ProcessEdge
from sqlalchemy.orm import Session


def _add_table(db, layer_node_id, name, description, columns, records):
    table = MasterTable(layer_node_id=layer_node_id, name=name, description=description, record_count=len(records))
    db.add(table)
    db.flush()
    for i, col in enumerate(columns):
        db.add(MasterColumn(master_table_id=table.id, display_order=i, **col))
    for i, rec in enumerate(records):
        db.add(MasterRecord(
            master_table_id=table.id,
            record_index=i,
            data=json.dumps(rec, ensure_ascii=False),
        ))
    return table


def seed_data(db: Session):
    if db.query(LayerNode).count() > 0:
        return

    # ==========================================================
    # Layer 1: 全社共通基幹システム
    # ==========================================================
    layer1 = LayerNode(name="全社共通基幹システム", description="全社で共通利用する基幹マスタデータ（部門別バリエーションあり）", layer_level=1)
    db.add(layer1)
    db.flush()

    # --- 社員マスタ ×3 バリエーション ---
    _add_table(db, layer1.id, "社員マスタ①（人事部）", "人事部が管理する正式な社員台帳",
        columns=[
            {"name": "社員番号", "column_type": "String", "is_required": True},
            {"name": "氏名", "column_type": "String", "is_required": True},
            {"name": "所属部門", "column_type": "String", "is_required": True},
            {"name": "役職", "column_type": "String"},
            {"name": "メールアドレス", "column_type": "String"},
            {"name": "入社日", "column_type": "Date", "is_required": True},
        ],
        records=[
            {"社員番号": "S10234", "氏名": "山田太郎", "所属部門": "建築事業部", "役職": "部長", "メールアドレス": "yamada.t@kensetsu.co.jp", "入社日": "2005-04-01"},
        ],
    )

    _add_table(db, layer1.id, "社員マスタ②（現場管理）", "現場で使用する作業員管理台帳",
        columns=[
            {"name": "作業員コード", "column_type": "String", "is_required": True},
            {"name": "名前", "column_type": "String", "is_required": True},
            {"name": "所属", "column_type": "String", "is_required": True},
            {"name": "職位", "column_type": "String"},
            {"name": "連絡先", "column_type": "String"},
            {"name": "配属日", "column_type": "Date"},
        ],
        records=[
            {"作業員コード": "W-10234", "名前": "山田太郎", "所属": "建築部", "職位": "現場所長", "連絡先": "090-1234-5678", "配属日": "2023-04-01"},
        ],
    )

    _add_table(db, layer1.id, "社員マスタ③（経理部）", "経理部の給与・経費管理用社員台帳",
        columns=[
            {"name": "従業員番号", "column_type": "String", "is_required": True},
            {"name": "氏名", "column_type": "String", "is_required": True},
            {"name": "部署コード", "column_type": "String", "is_required": True},
            {"name": "役職名", "column_type": "String"},
            {"name": "給与区分", "column_type": "String"},
        ],
        records=[
            {"従業員番号": "E10234", "氏名": "山田太郎", "部署コード": "D100", "役職名": "部長", "給与区分": "管理職A"},
        ],
    )

    # --- 取引先マスタ ×2 バリエーション ---
    _add_table(db, layer1.id, "取引先マスタ①（購買部）", "購買部が管理する取引先台帳",
        columns=[
            {"name": "取引先コード", "column_type": "String", "is_required": True},
            {"name": "会社名", "column_type": "String", "is_required": True},
            {"name": "代表者", "column_type": "String"},
            {"name": "住所", "column_type": "String"},
            {"name": "電話番号", "column_type": "String"},
            {"name": "取引区分", "column_type": "Picklist", "is_required": True},
        ],
        records=[
            {"取引先コード": "T00123", "会社名": "丸山鉄筋工業", "代表者": "丸山正夫", "住所": "東京都江東区新木場1-3-5", "電話番号": "03-3456-7890", "取引区分": "協力会社"},
        ],
    )

    _add_table(db, layer1.id, "取引先マスタ②（工事部）", "工事部が管理する業者台帳",
        columns=[
            {"name": "業者コード", "column_type": "String", "is_required": True},
            {"name": "企業名", "column_type": "String", "is_required": True},
            {"name": "担当者", "column_type": "String"},
            {"name": "所在地", "column_type": "String"},
            {"name": "TEL", "column_type": "String"},
            {"name": "業種分類", "column_type": "String", "is_required": True},
        ],
        records=[
            {"業者コード": "GC-0123", "企業名": "丸山鉄筋工業", "担当者": "中村浩二", "所在地": "東京都江東区新木場", "TEL": "03-3456-7890", "業種分類": "鉄筋工事"},
        ],
    )

    # --- 勘定科目マスタ ×2 バリエーション ---
    _add_table(db, layer1.id, "勘定科目マスタ①（本社経理）", "本社経理部の正式な勘定科目体系",
        columns=[
            {"name": "勘定科目コード", "column_type": "String", "is_required": True},
            {"name": "勘定科目名", "column_type": "String", "is_required": True},
            {"name": "科目区分", "column_type": "Picklist", "is_required": True},
            {"name": "補助科目", "column_type": "String"},
        ],
        records=[
            {"勘定科目コード": "5110", "勘定科目名": "材料費", "科目区分": "原価", "補助科目": "鉄筋材料"},
        ],
    )

    _add_table(db, layer1.id, "勘定科目マスタ②（工事原価）", "工事部門で使用する原価科目体系",
        columns=[
            {"name": "原価コード", "column_type": "String", "is_required": True},
            {"name": "原価科目", "column_type": "String", "is_required": True},
            {"name": "区分", "column_type": "String", "is_required": True},
            {"name": "細目", "column_type": "String"},
        ],
        records=[
            {"原価コード": "C-5110", "原価科目": "材料費", "区分": "直接原価", "細目": "主要材料"},
        ],
    )

    db.flush()

    # ==========================================================
    # Layer 2: 部門共通マスタ
    # ==========================================================
    layer2_construction = LayerNode(parent_id=layer1.id, name="工事部門共通マスタ", description="建築・土木工事部門で共通利用するマスタ", layer_level=2)
    db.add(layer2_construction)
    db.flush()

    # --- 協力会社マスタ ×2 バリエーション ---
    _add_table(db, layer2_construction.id, "協力会社マスタ①（建築部）", "建築部が管理する協力会社台帳",
        columns=[
            {"name": "会社名", "column_type": "String", "is_required": True},
            {"name": "担当者名", "column_type": "String"},
            {"name": "連絡先", "column_type": "String"},
            {"name": "専門工種", "column_type": "String", "is_required": True},
            {"name": "評価", "column_type": "Picklist"},
        ],
        records=[
            {"会社名": "丸山鉄筋工業", "担当者名": "中村浩二", "連絡先": "03-3456-7890", "専門工種": "鉄筋工事", "評価": "A"},
        ],
    )

    _add_table(db, layer2_construction.id, "協力会社マスタ②（土木部）", "土木部が管理する協力業者台帳",
        columns=[
            {"name": "企業名", "column_type": "String", "is_required": True},
            {"name": "担当者", "column_type": "String"},
            {"name": "電話番号", "column_type": "String"},
            {"name": "工事種別", "column_type": "String", "is_required": True},
            {"name": "ランク", "column_type": "Picklist"},
        ],
        records=[
            {"企業名": "丸山鉄筋工業", "担当者": "中村浩二", "電話番号": "03-3456-7890", "工事種別": "鉄筋", "ランク": "S"},
        ],
    )

    # --- 工種マスタ ×2 バリエーション ---
    _add_table(db, layer2_construction.id, "工種マスタ①（東京支店）", "東京支店で使用する工種分類",
        columns=[
            {"name": "工種コード", "column_type": "String", "is_required": True},
            {"name": "工種名", "column_type": "String", "is_required": True},
            {"name": "大分類", "column_type": "String", "is_required": True},
            {"name": "標準工期", "column_type": "Integer"},
            {"name": "標準単価", "column_type": "Integer"},
        ],
        records=[
            {"工種コード": "WK001", "工種名": "鉄筋工事", "大分類": "躯体", "標準工期": 14, "標準単価": 850000},
        ],
    )

    _add_table(db, layer2_construction.id, "工種マスタ②（大阪支店）", "大阪支店で使用する工事種別",
        columns=[
            {"name": "工事種別コード", "column_type": "String", "is_required": True},
            {"name": "工事種別名", "column_type": "String", "is_required": True},
            {"name": "カテゴリ", "column_type": "String", "is_required": True},
            {"name": "工期目安（日）", "column_type": "Integer"},
            {"name": "単価目安", "column_type": "Integer"},
        ],
        records=[
            {"工事種別コード": "K-001", "工事種別名": "鉄筋組立工事", "カテゴリ": "躯体工事", "工期目安（日）": 15, "単価目安": 880000},
        ],
    )

    db.flush()

    # --- Layer 2: 管理部門共通マスタ ---
    layer2_admin = LayerNode(parent_id=layer1.id, name="管理部門共通マスタ", description="安全・資格・品質管理で共通利用するマスタ", layer_level=2)
    db.add(layer2_admin)
    db.flush()

    _add_table(db, layer2_admin.id, "資格マスタ①（安全管理部）", "安全管理部が管理する資格台帳",
        columns=[
            {"name": "資格コード", "column_type": "String", "is_required": True},
            {"name": "資格名", "column_type": "String", "is_required": True},
            {"name": "種別", "column_type": "Picklist", "is_required": True},
            {"name": "有効期限", "column_type": "Date"},
        ],
        records=[
            {"資格コード": "Q001", "資格名": "1級建築施工管理技士", "種別": "国家資格", "有効期限": "無期限"},
        ],
    )

    _add_table(db, layer2_admin.id, "資格マスタ②（人材開発部）", "人材開発部が管理する資格・スキル台帳",
        columns=[
            {"name": "資格ID", "column_type": "String", "is_required": True},
            {"name": "資格名称", "column_type": "String", "is_required": True},
            {"name": "資格区分", "column_type": "String", "is_required": True},
            {"name": "更新期限", "column_type": "Date"},
            {"name": "取得難易度", "column_type": "String"},
        ],
        records=[
            {"資格ID": "SK-001", "資格名称": "一級建築施工管理技士", "資格区分": "国家", "更新期限": "不要", "取得難易度": "高"},
        ],
    )

    db.flush()

    # ==========================================================
    # Layer 3: 現場別マスタ
    # ==========================================================

    # --- 建築資材 ×3 バリエーション ---
    layer3_material = LayerNode(parent_id=layer2_construction.id, name="建築資材マスタ群", description="各現場・部門が個別管理する建築資材マスタ", layer_level=3)
    db.add(layer3_material)
    db.flush()

    _add_table(db, layer3_material.id, "建築資材マスタ①（豊洲現場）", "豊洲タワー現場の資材管理台帳",
        columns=[
            {"name": "品名", "column_type": "String", "is_required": True},
            {"name": "規格", "column_type": "String", "is_required": True},
            {"name": "単位", "column_type": "String", "is_required": True},
            {"name": "単価", "column_type": "Integer"},
            {"name": "在庫数量", "column_type": "Float"},
            {"name": "メーカー", "column_type": "String"},
        ],
        records=[
            {"品名": "ポルトランドセメント", "規格": "JIS R 5210", "単位": "t", "単価": 12500, "在庫数量": 85.0, "メーカー": "太平洋セメント"},
        ],
    )

    _add_table(db, layer3_material.id, "建築資材マスタ②（横浜現場）", "横浜駅北口再開発現場の資材台帳",
        columns=[
            {"name": "資材名", "column_type": "String", "is_required": True},
            {"name": "仕様", "column_type": "String", "is_required": True},
            {"name": "単位", "column_type": "String", "is_required": True},
            {"name": "価格", "column_type": "Integer"},
            {"name": "在庫数", "column_type": "Float"},
            {"name": "メーカ", "column_type": "String"},
        ],
        records=[
            {"資材名": "普通ポルトランドセメント", "仕様": "R5210準拠", "単位": "t", "価格": 12800, "在庫数": 120.0, "メーカ": "太平洋セメント"},
        ],
    )

    _add_table(db, layer3_material.id, "建築資材マスタ③（本社購買）", "本社購買部の資材マスタ（標準単価ベース）",
        columns=[
            {"name": "品目名称", "column_type": "String", "is_required": True},
            {"name": "規格型番", "column_type": "String", "is_required": True},
            {"name": "計量単位", "column_type": "String", "is_required": True},
            {"name": "標準単価", "column_type": "Integer"},
            {"name": "在庫量", "column_type": "Float"},
            {"name": "製造元", "column_type": "String"},
        ],
        records=[
            {"品目名称": "ポルトランドセメント", "規格型番": "JIS R 5210", "計量単位": "t", "標準単価": 12000, "在庫量": 350.0, "製造元": "太平洋セメント"},
        ],
    )

    # --- 建設機械 ×2 バリエーション ---
    layer3_equipment = LayerNode(parent_id=layer2_construction.id, name="建設機械マスタ群", description="各現場が個別管理する建設機械マスタ", layer_level=3)
    db.add(layer3_equipment)
    db.flush()

    _add_table(db, layer3_equipment.id, "建設機械マスタ①（A現場）", "豊洲タワー現場の機械台帳",
        columns=[
            {"name": "機種名", "column_type": "String", "is_required": True},
            {"name": "型式", "column_type": "String", "is_required": True},
            {"name": "能力", "column_type": "String", "is_required": True},
            {"name": "稼働状況", "column_type": "Picklist"},
            {"name": "日額単価", "column_type": "Integer"},
            {"name": "リース先", "column_type": "String"},
        ],
        records=[
            {"機種名": "ラフテレーンクレーン25t", "型式": "GR-250N-4", "能力": "25t吊", "稼働状況": "稼働中", "日額単価": 185000, "リース先": "アクティオ"},
        ],
    )

    _add_table(db, layer3_equipment.id, "建設機械マスタ②（B現場）", "横浜再開発現場の重機台帳",
        columns=[
            {"name": "重機名", "column_type": "String", "is_required": True},
            {"name": "型番", "column_type": "String", "is_required": True},
            {"name": "スペック", "column_type": "String", "is_required": True},
            {"name": "状況", "column_type": "Picklist"},
            {"name": "日額", "column_type": "Integer"},
            {"name": "レンタル会社", "column_type": "String"},
        ],
        records=[
            {"重機名": "ラフタークレーン25t", "型番": "GR-250N-4", "スペック": "吊能力25t", "状況": "使用中", "日額": 190000, "レンタル会社": "アクティオ"},
        ],
    )

    db.flush()

    # ==========================================================
    # Project (BPM)
    # ==========================================================
    project = Project(name="新築マンション建設工事", description="RC造10階建マンション新築工事", status="施工中", created_by="管理者")
    db.add(project)
    db.flush()

    nodes_data = [
        {"label": "着工準備", "node_type": "milestone", "position_x": 100, "position_y": 100, "duration_days": 7, "status": "完了"},
        {"label": "仮設工事", "node_type": "task", "position_x": 350, "position_y": 50, "duration_days": 14, "status": "完了"},
        {"label": "地盤改良", "node_type": "task", "position_x": 350, "position_y": 200, "duration_days": 21, "status": "施工中"},
        {"label": "基礎工事", "node_type": "task", "position_x": 600, "position_y": 100, "duration_days": 30, "status": "未着手"},
        {"label": "躯体工事（1F-5F）", "node_type": "task", "position_x": 850, "position_y": 50, "duration_days": 60, "status": "未着手"},
        {"label": "躯体工事（6F-10F）", "node_type": "task", "position_x": 850, "position_y": 200, "duration_days": 60, "status": "未着手"},
        {"label": "仕上工事", "node_type": "task", "position_x": 1100, "position_y": 100, "duration_days": 45, "status": "未着手"},
        {"label": "竣工検査", "node_type": "milestone", "position_x": 1350, "position_y": 100, "duration_days": 3, "status": "未着手"},
    ]

    created_nodes = []
    for nd in nodes_data:
        node = ProcessNode(project_id=project.id, **nd)
        db.add(node)
        db.flush()
        created_nodes.append(node)

    edges_data = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (3, 5), (4, 6), (5, 6), (6, 7)]
    for src_idx, tgt_idx in edges_data:
        edge = ProcessEdge(
            project_id=project.id,
            source_node_id=created_nodes[src_idx].id,
            target_node_id=created_nodes[tgt_idx].id,
        )
        db.add(edge)

    db.commit()
