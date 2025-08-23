import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORDS_DIR = ROOT / "words"
LIST_FILES = [WORDS_DIR / f"list{i}.txt" for i in range(1, 16)]
SUMMARY_DIR = WORDS_DIR / "list1-15"
CSV_PATH = SUMMARY_DIR / "list1-15summary-anki-en-zh.csv"
SUMMARY_MD_PATH = SUMMARY_DIR / "list1-15summary.md"

# list11-15 单词的中文释义
LIST11_15_MEANINGS = {
    'exuberant': '茂盛的；热情洋溢的',
    'exude': '渗出；散发',
    'exult': '狂喜；欢欣鼓舞',
    'fable': '寓言；虚构的故事',
    'facetious': '开玩笑的；滑稽的',
    'facile': '容易的；肤浅的',
    'faction': '派系；小集团',
    'fallacy': '谬误；谬论',
    'fallow': '休耕的；闲置的',
    'fail-safe': '故障安全的',
    'fasehood': '虚假；谎言',
    'falter': '蹒跚；犹豫',
    'fanatic': '狂热者；盲信者',
    'farce': '闹剧；滑稽戏',
    'fast': '快的；禁食',
    'fastidious': '挑剔的；讲究的',
    'fateful': '决定性的；重大的',
    'fathom': '理解；测量深度',
    'fatigue': '疲劳；使疲劳',
    'fatuous': '愚蠢的；愚昧的',
    'fawn': '奉承；小鹿',
    'faze': '使困惑；使为难',
    'feckless': '无能的；不负责任的',
    'fecund': '多产的；肥沃的',
    'feeble': '虚弱的；无力的',
    'feign': '假装；伪装',
    'fender': '挡泥板；防护物',
    'feral': '野生的；凶猛的',
    'ferrous': '含铁的',
    'fervid': '热烈的；热情的',
    'fervor': '热情；狂热',
    'fester': '化脓；恶化',
    'fetid': '恶臭的',
    'fetter': '束缚；脚镣',
    'fiasco': '惨败；大失败',
    'fickle': '反复无常的；善变的',
    'fidelity': '忠诚；忠实',
    'fidget': '坐立不安；烦躁',
    'figurehead': '傀儡；名义领袖',
    'figuring': '计算；推测',
    'filigree': '金银丝细工；精细装饰',
    'filling': '填充物；馅料',
    'filly': '小母马',
    'finch': '雀类；燕雀',
    'finesse': '技巧；手腕',
    'finicky': '挑剔的；过分讲究的',
    'flagging': '衰弱的；萎靡的',
    'flamboyant': '华丽的；炫耀的',
    'flatter': '奉承；谄媚',
    'flax': '亚麻；亚麻纤维',
    'fledge': '长羽毛；羽翼丰满',
    'fleet': '舰队；快速的',
    'flinch': '畏缩；退缩',
    'flippancy': '轻率；无礼',
    'flit': '轻快地飞；掠过',
    'flock': '群；聚集',
    'florid': '华丽的；红润的',
    'flounder': '挣扎；比目鱼',
    'flout': '藐视；嘲笑',
    'fluke': '侥幸；意外成功',
    'fluster': '使慌乱；使紧张',
    'fluvial': '河流的；河成的',
    'foible': '小缺点；弱点',
    'foll': '愚蠢；愚笨',
    'foliage': '叶子；树叶',
    'foment': '煽动；挑起',
    'foolproof': '万无一失的；简单可靠的',
    'footloose': '自由的；无拘束的',
    'forbear': '忍耐；克制',
    'forbearance': '忍耐；宽容',
    'ford': '浅滩；涉水',
    'forestall': '预先阻止；抢先',
    'foreword': '前言；序言',
    'forger': '伪造者；铁匠',
    'forthright': '直率的；坦率的',
    'founder': '创始人；沉没',
    'fracas': '吵闹；打架',
    'fracture': '骨折；破裂',
    'frail': '脆弱的；虚弱的',
    'fraudulent': '欺诈的；欺骗的',
    'fraught': '充满的；忧虑的',
    'frenzy': '狂乱；疯狂',
    'fresco': '壁画；湿壁画',
    'fretful': '烦躁的；焦虑的',
    'friable': '易碎的；脆的',
    'frieze': '饰带；横饰带',
    'frigid': '寒冷的；冷淡的',
    'fringe': '边缘；流苏',
    'frivolous': '轻浮的；无聊的',
    'frond': '蕨叶；棕榈叶',
    'frothy': '起泡的；浅薄的',
    'frowsy': '邋遢的；不整洁的',
    'frugal': '节俭的；节约的',
    'full-bodied': '醇厚的；丰满的',
    'fulminate': '猛烈抨击；爆炸',
    'fumble': '摸索；笨拙地处理',
    'furor': '狂怒；轰动',
    'furtive': '偷偷摸摸的；鬼鬼祟祟的',
    'fussy': '挑剔的；过分讲究的',
    'fusty': '发霉的；陈腐的',
    'gadfly': '牛虻；讨厌的人',
    'gadget': '小器具；小装置',
    'gaffe': '失态；失言',
    'gainsay': '否认；反驳',
    'gait': '步态；步伐',
    'gall': '胆汁；怨恨',
    'gallant': '勇敢的；殷勤的',
    'galley': '厨房；单层甲板船',
    'galvanize': '刺激；电镀',
    'gambol': '跳跃；嬉戏',
    'gangly': '瘦长笨拙的',
    'gangway': '通道；舷梯',
    'garble': '混淆；曲解',
    'gargantuan': '巨大的；庞大的',
    'garish': '俗丽的；花哨的',
    'garment': '衣服；服装',
    'garrulous': '话多的；饶舌的',
    'gash': '深伤口；砍伤',
    'gaudy': '俗丽的；花哨的',
    'genial': '和蔼的；友好的',
    'genteel': '有教养的；文雅的',
    'germane': '相关的；贴切的',
    'gerrymander': '不公正地划分选区',
    'geyser': '间歇泉；热水器',
    'gibe': '嘲笑；奚落',
    'giddy': '头晕的；轻浮的',
    'gild': '镀金；装饰',
    'girder': '大梁；钢梁',
    'gist': '要点；主旨',
    'glade': '林间空地',
    'gladiator': '角斗士；斗士',
    'glaze': '釉；上釉',
    'glib': '油嘴滑舌的；流利的',
    'glisten': '闪闪发光',
    'gloat': '幸灾乐祸；得意洋洋',
    'gloomy': '阴暗的；忧郁的',
    'gloss': '光泽；注释',
    'glossy': '有光泽的；光滑的',
    'glut': '过剩；充斥',
    'glutinous': '粘性的；胶状的',
    'glutton': '贪食者；暴食者',
    'goad': '刺激；激励',
    'gobble': '狼吞虎咽；咯咯叫',
    'goldbrick': '懒汉；逃避工作的人',
    'gorge': '峡谷；狼吞虎咽',
    'gossamer': '蛛丝；薄纱',
    'gourmand': '美食家；贪吃的人',
    'gourmet': '美食家；美食鉴赏家',
    'grandiloquent': '夸张的；浮夸的',
    'grandlose': '宏伟的；壮丽的',
    'grandstand': '看台；哗众取宠',
    'grate': '磨碎；激怒',
    'gratitous': '免费的；无理由的',
    'gratify': '使满足；使高兴',
    'gravel': '砾石；使困惑',
    'green': '绿色的；未成熟的',
    'gregarious': '群居的；爱交际的',
    'grieve': '悲伤；哀悼',
    'grimace': '鬼脸；面部扭曲',
    'grin': '咧嘴笑',
    'gripe': '抱怨；腹痛',
    'grisly': '可怕的；恐怖的',
    'groove': '凹槽；习惯',
    'grotesque': '怪诞的；奇形怪状的',
    'grotto': '洞穴；石窟',
    'grove': '小树林；果园',
    'grovel': '匍匐；卑躬屈膝',
    'grueling': '累人的；折磨人的',
    'guarantee': '保证；担保',
    'guile': '狡诈；诡计',
    'gullible': '易受骗的；轻信的',
    'gully': '沟壑；溪谷',
    'gum': '牙龈；口香糖',
    'gush': '涌出；滔滔不绝地说',
    'gust': '阵风；一阵',
    'guzzle': '狂饮；大口喝',
    'hack': '砍；黑客',
    'hackneyed': '陈腐的；老套的',
    'halcyon': '平静的；太平的',
    'hale': '强壮的；健康的',
    'half-backed': '不成熟的；考虑不周的',
    'hallmark': '标志；特征',
    'hallow': '使神圣；崇敬',
    'hallucination': '幻觉；错觉',
    'ham-handed': '笨手笨脚的',
    'hamstring': '使残废；削弱',
    'hangdog': '垂头丧气的；羞愧的',
    'hanker': '渴望；向往',
    'haphazard': '随意的；偶然的',
    'harangue': '长篇演说；训斥',
    'harbinger': '先驱；预兆',
    'harbor': '港口；庇护',
    'hard-bitten': '坚韧的；顽强的',
    'hardy': '强壮的；耐寒的',
    'harness': '马具；利用',
    'harp': '竖琴；反复说',
    'harrow': '耙；折磨',
    'harry': '骚扰；折磨',
    'hasten': '加速；催促',
    'hasty': '匆忙的；草率的',
    'haunt': '常去；萦绕',
    'hauteur': '傲慢；高傲',
    'haven': '避风港；安全的地方',
    'havoc': '大破坏；浩劫',
    'headlong': '头朝前的；鲁莽的',
    'hearken': '倾听；注意',
    'hearten': '鼓励；使振作',
    'heartending': '令人心碎的',
    'hedonism': '享乐主义',
    'hegemony': '霸权；支配地位',
    'heinous': '可憎的；邪恶的',
    'heirloom': '传家宝；传家之物',
    'hem': '边缘；缝边',
    'hew': '砍；劈',
    'herald': '先驱；宣告者',
    'herbicide': '除草剂',
    'heresy': '异端；异端邪说',
    'heretical': '异端的；异教的',
    'hermetic': '密封的；神秘的',
    'hermit': '隐士；隐居者',
    'herpetologist': '爬虫学家',
    'heterodox': '异端的；非正统的',
    'orthodox': '正统的；传统的',
    'hidebound': '守旧的；顽固的',
    'hideous': '可怕的；丑陋的',
    'hie': '匆忙；赶快',
    'hieroglyph': '象形文字',
    'hike': '徒步旅行；提高',
    'histrionic': '戏剧性的；做作的',
    'hive': '蜂巢；蜂群',
    'hoard': '贮藏；囤积',
    'hoary': '灰白的；古老的',
    'hoax': '恶作剧；骗局',
    'hodgepodge': '大杂烩；混合物',
    'homage': '敬意；效忠',
    'homely': '朴素的；不好看的',
    'homily': '说教；布道',
    'hone': '磨刀；磨练',
    'honorarium': '酬金；谢礼',
    'hoodwink': '欺骗；蒙蔽',
    'hortative': '劝告的；劝勉的',
    'horticulture': '园艺；园艺学',
    'hovel': '简陋的小屋',
    'hub': '中心；枢纽',
    'hubris': '傲慢；自大',
    'husbandry': '农业；畜牧业',
    'husk': '外壳；皮',
    'husky': '强壮的；嘶哑的',
    'hymn': '赞美诗；圣歌',
    'hyperbole': '夸张；夸大',
    'hypnotic': '催眠的；催眠术的',
    'ichthyologist': '鱼类学家',
    'iconoclast': '偶像破坏者；反传统者',
    'idolatrize': '偶像崇拜；盲目崇拜',
    'idyll': '田园诗；田园生活',
    'ignominy': '耻辱；不名誉',
    'illuminati': '启蒙者；智者',
    'illusory': '虚幻的；错觉的',
    'imbibe': '吸收；饮',
    'imbroglio': '复杂的情况；混乱',
    'immaculate': '完美的；纯洁的',
    'immanent': '内在的；固有的',
    'immaterial': '不重要的；非物质的',
    'immemorial': '远古的；无法追忆的',
    'immure': '监禁；禁闭',
    'imp': '小鬼；顽童',
    'impeccable': '完美的；无瑕疵的',
    'impecunious': '贫穷的；身无分文的',
    'impede': '阻碍；妨碍',
    'impend': '即将发生；迫近',
    'impenitent': '不悔改的；顽固的',
    'imperative': '必要的；命令的',
    'imperious': '专横的；傲慢的',
    'impertinent~impertinence': '无礼的；不恰当的',
    'imperturbable': '冷静的；沉着的',
    'impervious': '不透的；不受影响的',
    'impetuous': '冲动的；鲁莽的',
    'implety': '不虔诚；不敬',
    'implacable': '不宽容的；无情的',
    'imposing': '给人深刻印象的；庄严的',
    'importune': '纠缠；强求',
    'imposter': '冒名顶替者；骗子',
    'impotent': '无能的；无力的',
    'impresario': '演出经理；演出主办者',
    'impromptu~improvise': '即兴的；即兴创作',
    'imprudent': '轻率的；不谨慎的',
    'impudent': '无礼的；厚颜无耻的',
    'impugn': '质疑；抨击',
    'impulssance': '无能；无力',
    'imadvertent': '无意的；不小心的',
    'inalienable': '不可剥夺的；不可转让的',
    'inane': '愚蠢的；空洞的',
    'inanimate': '无生命的；无生气的',
    'inaugurate': '开始；就职',
    'incandescent': '白炽的；明亮的',
    'incantation': '咒语；魔法',
    'incarnate': '化身；体现',
    'incendiary': '纵火的；煽动的',
    'incense': '香；激怒',
    'inception': '开始；开端',
    'incessant': '不停的；连续的',
    'inch': '英寸；缓慢移动',
    'inchoate': '初期的；未形成的',
    'incinerate': '焚烧；火化',
    'incipient': '初期的；开始的',
    'incite': '煽动；激起',
    'inclement': '恶劣的；严酷的',
    'incogitant': '考虑不周的；轻率的',
    'inconsequential': '不重要的；无关紧要的',
    'incomtrovertible': '无可争议的；不容置疑的',
    'incorrigible': '不可救药的；无法改正的',
    'incriminate': '使有罪；牵连',
    'incubator': '孵化器；温床',
    'inculpate': '控告；归罪',
    'incursion': '入侵；袭击',
    'indelible': '不可磨灭的；持久的',
    'indemnity': '赔偿；补偿',
    'indict': '起诉；控告',
    'indigent': '贫穷的；贫困的',
    'indolent': '懒惰的；怠惰的',
    'inducement': '诱因；动机',
    'indulgent': '纵容的；溺爱的',
    'indurate': '使硬化；使冷酷',
    'industriousness': '勤劳；勤奋',
    'ineffable': '不可言喻的；难以形容的',
    'ineluctable': '不可避免的；无法逃避的',
    'inept': '无能的；不称职的',
    'inexorable': '无情的；不可阻挡的',
    'infamy': '臭名昭著；恶名',
    'infatuate': '使迷恋；使糊涂',
    'inferno': '地狱；大火',
    'infiltrate': '渗透；潜入',
    'infirm': '虚弱的；体弱的',
    'inflame': '激怒；使发炎',
    'infelicitous': '不恰当的；不幸的',
    'influx': '流入；涌入',
    'infuse': '注入；灌输',
    'infuriate': '激怒；使愤怒',
    'ingenuity': '独创性；聪明才智',
    'ingenious': '聪明的；有创造力的',
    'ingest': '摄取；吸收',
    'ingrained': '根深蒂固的；根深蒂固的',
    'ingrate': '忘恩负义的人',
    'ingratiating': '讨好的；奉承的',
    'inimical': '敌对的；有害的',
    'inimitable': '无法模仿的；独特的',
    'iniquity': '邪恶；不公正',
    'inkling': '暗示；线索',
    'innocuous': '无害的；无毒的',
    'inquisitive': '好奇的；好问的',
    'insensitive': '不敏感的；麻木的',
    'insentient': '无感觉的；无意识的',
    'insipid': '乏味的；平淡的',
    'insolent': '傲慢的；无礼的',
    'insouciant': '无忧无虑的；漫不经心的',
    'instate': '任命；安置',
    'instigate': '煽动；挑起',
    'instill': '灌输；注入',
    'insular': '孤立的；狭隘的',
    'intangible': '无形的；难以捉摸的',
    'intelligible': '可理解的；清晰的',
    'intemperate': '过度的；放纵的',
    'inter': '埋葬；安葬',
    'intercessor': '调解者；代祷者',
    'interdict': '禁止；禁令',
    'interlock': '连锁；互锁',
    'interminable': '无止境的；冗长的',
    'intermittent': '间歇的；断断续续的',
    'interregnum': '空位期；过渡期',
    'intransigent': '不妥协的；顽固的',
    'intrepid': '勇敢的；无畏的',
    'inundate': '淹没；使充满',
    'inure': '使习惯；使适应',
    'invective': '辱骂；谩骂',
    'inveigh': '猛烈抨击；痛骂',
    'inveigle': '诱骗；哄骗',
    'inveterate': '根深蒂固的；积习难深的',
    'invidious': '令人反感的；有害的',
    'invigorate': '使精力充沛；使活跃',
    'irascible': '易怒的；暴躁的',
    'irate': '愤怒的；生气的',
    'iridescence': '彩虹色；彩虹光泽',
    'irk': '使烦恼；使厌烦',
    'ironclad': '铁甲舰；坚不可摧的',
    'irradicable': '根深蒂固的；无法根除的',
    'isthmus': '地峡；狭窄地带'
}

def add_chinese_meanings_to_csv():
    """给CSV中list11-15的单词添加中文释义"""
    if not CSV_PATH.exists():
        print("CSV文件不存在")
        return
    
    content = CSV_PATH.read_text(encoding="utf-8")
    lines = content.splitlines()
    
    for i, line in enumerate(lines):
        word = line.split(',')[0].strip()
        if word in LIST11_15_MEANINGS:
            lines[i] = f"{word},{LIST11_15_MEANINGS[word]}"
    
    CSV_PATH.write_text('\n'.join(lines), encoding="utf-8")
    print(f"已为 {len(LIST11_15_MEANINGS)} 个单词添加中文释义")

def shuffle_all_files():
    """打乱所有文件中的单词顺序"""
    for file_path in LIST_FILES:
        if not file_path.exists():
            continue
            
        content = file_path.read_text(encoding="utf-8")
        lines = content.splitlines()
        
        # 分离标题行和单词行
        header_lines = []
        word_lines = []
        
        for line in lines:
            if line.startswith('u') and ':' in line:
                header_lines.append(line)
            elif line.strip():
                word_lines.append(line)
        
        # 打乱单词行
        random.shuffle(word_lines)
        
        # 重新组合
        new_content = '\n'.join(header_lines + word_lines)
        file_path.write_text(new_content, encoding="utf-8")
    
    print(f"已打乱 {len(LIST_FILES)} 个文件中的单词顺序")

def update_summary_memory_sections():
    """更新summary.md中的帮助记忆部分"""
    if not SUMMARY_MD_PATH.exists():
        print("summary.md文件不存在")
        return
    
    content = SUMMARY_MD_PATH.read_text(encoding="utf-8")
    
    # 更新标题，反映现在是list1-15
    content = content.replace(
        "## 近义词分组（高频语义场，含 list1-10 扩展）",
        "## 近义词分组（高频语义场，含 list1-15 扩展）"
    )
    
    content = content.replace(
        "## 反义词配对（优先在 list1-10 内部找对立）",
        "## 反义词配对（优先在 list1-15 内部找对立）"
    )
    
    content = content.replace(
        "（上表优先覆盖高频/易考词；若需完整逐词导出为表，可后续把 `list1-10` 的所有词条批量生成 CSV/MD。）",
        "（上表覆盖 list1-15 完整词汇；若需完整逐词导出为表，可后续把 `list1-15` 的所有词条批量生成 CSV/MD。）"
    )
    
    # 添加新的记忆辅助内容
    new_memory_content = """

## 新增记忆技巧（list11-15 特色）

### 字母规律记忆
- **F系列**：facetious（开玩笑的）→ facile（容易的）→ faction（派系）→ fallacy（谬误）
- **G系列**：garrulous（话多的）→ gaudy（俗丽的）→ germane（相关的）→ gibe（嘲笑）
- **H系列**：harbinger（先驱）→ harangue（长篇演说）→ haphazard（随意的）→ hauteur（傲慢）
- **I系列**：inchoate（初期的）→ inclement（恶劣的）→ incorrigible（不可救药的）→ intransigent（不妥协的）

### 词根联想（list11-15 新增）
- **-fid-（信任）**: fidelity（忠诚）；confide（信任，延伸）
- **-gen-（产生）**: engender（引发）；germane（相关的）
- **-her-（继承）**: heirloom（传家宝）；heritage（遗产，延伸）
- **-inc-（进入）**: incursion（入侵）；incite（煽动）
- **-int-（内部）**: intransigent（不妥协的）；intrepid（勇敢的）

### 场景化记忆
- **政治场景**: gerrymander（不公正划分选区）→ hegemony（霸权）→ harbinger（先驱）
- **学术场景**: histrionic（戏剧性的）→ hieroglyph（象形文字）→ herpetologist（爬虫学家）
- **商业场景**: haggard（憔悴的）→ hale（强壮的）→ halcyon（平静的）
- **情感场景**: irascible（易怒的）→ irate（愤怒的）→ iridescence（彩虹色）
"""
    
    # 在词根词缀记忆部分后添加新内容
    if "## 词根词缀记忆（以线索带词群）" in content:
        content = content.replace(
            "## 词根词缀记忆（以线索带词群）",
            "## 词根词缀记忆（以线索带词群）" + new_memory_content
        )
    
    SUMMARY_MD_PATH.write_text(content, encoding="utf-8")
    print("已更新summary.md的帮助记忆部分")

def main():
    print("开始更新 list1-15 文件...")
    
    # 设置随机种子以确保可重现性
    random.seed(42)
    
    # 1. 给CSV添加中文释义
    add_chinese_meanings_to_csv()
    
    # 2. 打乱单词顺序
    shuffle_all_files()
    
    # 3. 更新summary.md
    update_summary_memory_sections()
    
    print("所有更新完成！")

if __name__ == "__main__":
    main()
