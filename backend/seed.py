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
            {"社員番号": "S10567", "氏名": "鈴木一郎", "所属部門": "土木事業部", "役職": "課長", "メールアドレス": "suzuki.i@kensetsu.co.jp", "入社日": "2010-04-01"},
            {"社員番号": "S20891", "氏名": "佐藤美咲", "所属部門": "設備事業部", "役職": "主任", "メールアドレス": "sato.m@kensetsu.co.jp", "入社日": "2015-04-01"},
            {"社員番号": "S30124", "氏名": "高橋健太", "所属部門": "建築事業部", "役職": "係長", "メールアドレス": "takahashi.k@kensetsu.co.jp", "入社日": "2012-10-01"},
            {"社員番号": "S30456", "氏名": "渡辺直子", "所属部門": "管理本部", "役職": "課長", "メールアドレス": "watanabe.n@kensetsu.co.jp", "入社日": "2008-04-01"},
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
            {"作業員コード": "W-10567", "名前": "鈴木一郎", "所属": "土木部", "職位": "主任技術者", "連絡先": "090-2345-6789", "配属日": "2023-06-01"},
            {"作業員コード": "W-20891", "名前": "佐藤美咲", "所属": "設備部", "職位": "工事主任", "連絡先": "090-3456-7890", "配属日": "2024-01-15"},
            {"作業員コード": "W-30124", "名前": "高橋健太", "所属": "建築部", "職位": "現場監督", "連絡先": "090-4567-8901", "配属日": "2023-09-01"},
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
            {"従業員番号": "E10567", "氏名": "鈴木一郎", "部署コード": "D200", "役職名": "課長", "給与区分": "管理職B"},
            {"従業員番号": "E20891", "氏名": "佐藤美咲", "部署コード": "D300", "役職名": "主任", "給与区分": "一般職A"},
            {"従業員番号": "E30124", "氏名": "高橋健太", "部署コード": "D100", "役職名": "係長", "給与区分": "一般職A"},
            {"従業員番号": "E30456", "氏名": "渡辺直子", "部署コード": "D400", "役職名": "課長", "給与区分": "管理職B"},
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
            {"取引先コード": "T00456", "会社名": "東海型枠株式会社", "代表者": "田中誠", "住所": "神奈川県横浜市鶴見区大黒町5-20", "電話番号": "045-678-9012", "取引区分": "協力会社"},
            {"取引先コード": "T00789", "会社名": "太平洋セメント株式会社", "代表者": "山本健一", "住所": "東京都港区台場2-3-1", "電話番号": "03-5531-7111", "取引区分": "資材業者"},
            {"取引先コード": "T01023", "会社名": "アクティオ株式会社", "代表者": "小沢直義", "住所": "東京都中央区日本橋3-12-2", "電話番号": "03-3279-0621", "取引区分": "リース"},
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
            {"業者コード": "GC-0456", "企業名": "東海型枠", "担当者": "小林正樹", "所在地": "横浜市鶴見区", "TEL": "045-678-9012", "業種分類": "型枠工事"},
            {"業者コード": "GC-0789", "企業名": "太平洋セメント", "担当者": "高橋義男", "所在地": "港区台場", "TEL": "03-5531-7111", "業種分類": "資材供給"},
            {"業者コード": "GC-1023", "企業名": "アクティオ", "担当者": "田村隆", "所在地": "中央区日本橋", "TEL": "03-3279-0621", "業種分類": "機械リース"},
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
            {"勘定科目コード": "5120", "勘定科目名": "労務費", "科目区分": "原価", "補助科目": "直接労務"},
            {"勘定科目コード": "5130", "勘定科目名": "外注費", "科目区分": "原価", "補助科目": "躯体工事"},
            {"勘定科目コード": "5210", "勘定科目名": "経費", "科目区分": "原価", "補助科目": "現場経費"},
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
            {"原価コード": "C-5120", "原価科目": "労務費", "区分": "直接原価", "細目": "技能工"},
            {"原価コード": "C-5130", "原価科目": "外注費", "区分": "直接原価", "細目": "専門工事"},
            {"原価コード": "C-5210", "原価科目": "現場経費", "区分": "間接原価", "細目": "仮設材"},
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
            {"会社名": "東海型枠", "担当者名": "小林正樹", "連絡先": "045-678-9012", "専門工種": "型枠工事", "評価": "A"},
            {"会社名": "日本クレーン", "担当者名": "高橋義男", "連絡先": "03-5544-1111", "専門工種": "揚重工事", "評価": "B"},
            {"会社名": "関東塗装工業", "担当者名": "伊藤大輔", "連絡先": "048-234-5678", "専門工種": "塗装工事", "評価": "A"},
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
            {"企業名": "東海型枠", "担当者": "小林正樹", "電話番号": "045-678-9012", "工事種別": "型枠", "ランク": "A"},
            {"企業名": "日本クレーン", "担当者": "高橋義男", "電話番号": "03-5544-1111", "工事種別": "揚重", "ランク": "A"},
            {"企業名": "関東塗装", "担当者": "伊藤大輔", "電話番号": "048-234-5678", "工事種別": "塗装", "ランク": "B"},
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
            {"工種コード": "WK002", "工種名": "型枠工事", "大分類": "躯体", "標準工期": 21, "標準単価": 1200000},
            {"工種コード": "WK003", "工種名": "コンクリート工事", "大分類": "躯体", "標準工期": 7, "標準単価": 650000},
            {"工種コード": "WK004", "工種名": "防水工事", "大分類": "仕上", "標準工期": 10, "標準単価": 480000},
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
            {"工事種別コード": "K-002", "工事種別名": "型枠建込工事", "カテゴリ": "躯体工事", "工期目安（日）": 22, "単価目安": 1250000},
            {"工事種別コード": "K-003", "工事種別名": "コンクリ打設", "カテゴリ": "躯体工事", "工期目安（日）": 8, "単価目安": 680000},
            {"工事種別コード": "K-004", "工事種別名": "防水施工", "カテゴリ": "仕上工事", "工期目安（日）": 12, "単価目安": 500000},
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
            {"資格コード": "Q002", "資格名": "1級土木施工管理技士", "種別": "国家資格", "有効期限": "無期限"},
            {"資格コード": "Q003", "資格名": "足場の組立作業主任者", "種別": "技能資格", "有効期限": "2027-03-31"},
            {"資格コード": "Q004", "資格名": "玉掛け技能講習", "種別": "技能資格", "有効期限": "無期限"},
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
            {"資格ID": "SK-002", "資格名称": "一級土木施工管理技士", "資格区分": "国家", "更新期限": "不要", "取得難易度": "高"},
            {"資格ID": "SK-003", "資格名称": "足場組立作業主任者", "資格区分": "講習", "更新期限": "5年", "取得難易度": "中"},
            {"資格ID": "SK-004", "資格名称": "玉掛技能", "資格区分": "講習", "更新期限": "不要", "取得難易度": "低"},
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
            {"品名": "異形棒鋼D16", "規格": "JIS G 3112 SD345", "単位": "本", "単価": 980, "在庫数量": 14200, "メーカー": "東京製鐵"},
            {"品名": "合板型枠12mm", "規格": "JIS A 5908", "単位": "枚", "単価": 1850, "在庫数量": 8500, "メーカー": "大建工業"},
            {"品名": "H形鋼200x200", "規格": "JIS G 3192", "単位": "kg", "単価": 125, "在庫数量": 32000.0, "メーカー": "JFEスチール"},
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
            {"資材名": "異形棒鋼D16", "仕様": "SD345 JIS準拠", "単位": "本", "価格": 1020, "在庫数": 8900, "メーカ": "東京製鐵"},
            {"資材名": "合板型枠12mm", "仕様": "JIS規格品", "単位": "枚", "価格": 1900, "在庫数": 5200, "メーカ": "大建工業"},
            {"資材名": "H型鋼200x200", "仕様": "JIS G3192", "単位": "kg", "価格": 130, "在庫数": 18500.0, "メーカ": "JFEスチール"},
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
            {"品目名称": "異形棒鋼D16", "規格型番": "JIS G 3112 SD345", "計量単位": "本", "標準単価": 950, "在庫量": 45000, "製造元": "東京製鐵"},
            {"品目名称": "型枠合板12mm", "規格型番": "JIS A 5908", "計量単位": "枚", "標準単価": 1800, "在庫量": 22000, "製造元": "大建工業"},
            {"品目名称": "H形鋼200×200", "規格型番": "JIS G 3192", "計量単位": "kg", "標準単価": 120, "在庫量": 85000.0, "製造元": "JFEスチール"},
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
            {"機種名": "タワークレーン", "型式": "CT-500", "能力": "最大揚程50m", "稼働状況": "稼働中", "日額単価": 320000, "リース先": "カナモト"},
            {"機種名": "油圧ショベル0.7m³", "型式": "PC200-10", "能力": "バケット0.7m³", "稼働状況": "待機中", "日額単価": 95000, "リース先": "レンタルのニッケン"},
            {"機種名": "コンクリートポンプ車", "型式": "BSF36Z", "能力": "ブーム長36m", "稼働状況": "稼働中", "日額単価": 250000, "リース先": "アクティオ"},
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
            {"重機名": "タワークレーン", "型番": "CT-500", "スペック": "揚程50m", "状況": "使用中", "日額": 330000, "レンタル会社": "カナモト"},
            {"重機名": "バックホウ0.7", "型番": "PC200-10", "スペック": "0.7m³バケット", "状況": "待機", "日額": 98000, "レンタル会社": "ニッケン"},
            {"重機名": "ポンプ車36m", "型番": "BSF36Z", "スペック": "36mブーム", "状況": "使用中", "日額": 260000, "レンタル会社": "アクティオ"},
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
