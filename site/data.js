export const sources = [
  {id:'S1', title:'中央红军撤离中央根据地开始长征', publisher:'中国军网', url:'https://www.81.mil.cn/2018byzt/2018-07/31/content_8099891.htm', note:'1934年出发与长征主要时间节点；如入口失效，可结合S2核对。'},
  {id:'S2', title:'遵义会议和红军长征的胜利', publisher:'工业和信息化部／共产党员网', url:'https://www.miit.gov.cn/ztzl/rdzt/dsxxjyzl/xxzl/art/2021/art_a43d76bc5e694806889c07fc36ec6adc.html', note:'长征历程、路线调整与遵义会议。'},
  {id:'S3', title:'长征七易落脚点', publisher:'中国军网', url:'https://www.81.cn/yljnt_208627/lsda_208656/16375724.html', note:'长征中的方向调整与道路探索。'},
  {id:'S4', title:'红军抵达陕北吴起镇，红一方面军长征胜利结束', publisher:'中央网信办', url:'https://www.cac.gov.cn/2016-08/22/c_1119432438.htm', note:'1935年10月抵达吴起。'},
  {id:'S5', title:'西迁精神：爱国奋斗的情怀', publisher:'西安交大西迁精神专题网／中国人才', url:'https://xq.xjtu.edu.cn/info/1010/1201.htm', note:'迁校背景、乘车证与西迁精神概括。'},
  {id:'S6', title:'校史故事365：在西去的列车上', publisher:'西安交通大学新闻网', url:'https://news.xjtu.edu.cn/info/1033/11188.htm', note:'郑善维回忆，原载2001年《交通大学西迁回忆录》。南京轮渡与留校经历据此改写。'},
  {id:'S7', title:'三军大会师——红军长征三大主力会师全纪录', publisher:'中央网信办', url:'https://www.cac.gov.cn/2016-08/22/c_1119432029.htm', note:'1936年三大主力会师。'},
  {id:'S8', title:'1956年9月10日迁校后的首次开学典礼', publisher:'西安交大·西迁记忆', url:'https://xqjy.xjtu.edu.cn/info/1063/1246.htm', note:'首次开学典礼的时间与地点。'},
  {id:'S9', title:'习近平给四所交通大学全体师生的回信', publisher:'新华网', url:'https://www.xinhuanet.com/politics/20260407/93ffd51c2a1449ebb82f84235b005ab1/c.html', note:'2026年4月7日，写给上海交大、西安交大、西南交大、北京交大全体师生。'},
  {id:'S11', title:'1956年8月从上海徐家汇启程', publisher:'西安交大·西迁记忆', url:'https://xqjy.xjtu.edu.cn/info/1063/1245.htm', note:'出发档案图片与事件记载。'},
  {id:'S12', title:'1956年9月2日乘车证', publisher:'西安交大西迁精神专题网', url:'https://xq.xjtu.edu.cn/info/1022/2508.htm', note:'西迁乘车证档案图片。'},
  {id:'S13', title:'“重走长征路 奋进新征程”教职工健步走活动启动', publisher:'西安交通大学新闻网', url:'https://news.xjtu.edu.cn/info/1007/230870.htm', note:'2026年4月10日活动，4月11日报道；图片署名校工会。'},
];

export const chapters = [
  {id:'P0', title:'两次出发', period:'山河之间 · 两次出发', march:9, west:5, focus:[], huining:true, mode:'overview'},
  {id:'P1', title:'道路从困境中展开', period:'1934.10 — 1935.01', march:2, west:0, focus:['yudu','xiangjiang','zunyi'], huining:false, mode:'march'},
  {id:'P2', title:'在曲折中争取主动', period:'1935 · 江河与雪山', march:7, west:0, focus:['zunyi','jinshajiang','luding','grass-region'], huining:false, mode:'march'},
  {id:'P3', title:'抵达，是新的开始', period:'1935 / 1936 · 抵达与会师', march:9, west:0, focus:['wuqi'], huining:true, mode:'march'},
  {id:'P4', title:'建设年代的回答', period:'1955 — 1956 · 新的任务', march:9, west:0, focus:['shanghai'], huining:false, mode:'transition'},
  {id:'P5', title:'列车把课堂带向西部', period:'1956 · 夏 · 西行专列', march:9, west:5, focus:['shanghai','nanjing','tongguan','xian'], huining:false, mode:'west'},
  {id:'P6', title:'到达之后，才是扎根', period:'1956年起 · 办学与扎根', march:9, west:5, focus:['xian'], huining:false, mode:'west'},
  {id:'P7', title:'把精神写进今天的行动', period:'2026 · 回信与接续', march:9, west:5, focus:['wuqi','xian'], huining:true, mode:'overview'},
];

export const details = {
  route: {
    eyebrow:'长征 · 道路探索', title:'为什么路线会改变？',
    paragraphs:[
      '长征的前进方向并非从出发时就固定不变。湘江战役之后，红军根据敌情与自身处境调整行动。遵义会议前后的探索说明：坚定目标与根据实际情况改变走法，并不矛盾。',
      '地图上的线经过事后整理，才显得完整。理解这段历程，也需要看见当时判断形势、发现问题与纠正错误的过程。'
    ], sourceIds:['S2','S3'],
  },
  ferry: {
    eyebrow:'西迁 · 一趟专列的细节', title:'南京：火车也要坐船过江',
    paragraphs:[
      '郑善维在《在西去的列车上》中回忆，1956年8月10日出发的专列到达南京后，师生下车，观看车厢被分开送上渡船、运过长江，然后接续行程。',
      '这个细节呈现了当时迁移工作的具体条件。它属于一趟专列的回忆，不代表所有西迁批次拥有完全相同的时间与行程。下图据文字绘制，不是历史现场复原。'
    ], sourceIds:['S6'], illustration:'ferry',
  },
  rooted: {
    eyebrow:'西迁 · 时间的尺度', title:'从一趟列车，到一生扎根',
    paragraphs:[
      '郑善维记述，抵达西安后，他在交大校园学习成长，毕业后留校工作直至退休。',
      '迁移可以在地图上用一条线标出，扎根却需要用更长的时间理解。一次出发，延伸成日复一日的教学、研究、工作与生活。'
    ], sourceIds:['S6'],
  },
  geography: {
    eyebrow:'山河之间', title:'两条道路，两次出发',
    paragraphs:[
      '从于都出发，中央红军历经艰险，在1935年抵达陕北吴起；1936年，三大主力红军胜利会师。',
      '从上海出发，交大师生员工在1956年分批赴西安，开启扎根西部的建设历程。',
      '吴起与西安，分别记录着两次重要的抵达。将两条道路放在一起，是为了理解不同年代中相通的信念与担当。'
    ], sourceIds:['S2','S6','S7'],
  },
};

export const photos = {
  ticket:{file:'ticket-1956.jpg',title:'一张乘车证，一次西行',caption:'1956年9月2日乘车证',credit:'西安交通大学西迁精神专题网',url:'https://xq.xjtu.edu.cn/info/1022/2508.htm',sourceId:'S12'},
  departure:{file:'departure-1956.jpeg',title:'从徐家汇启程',caption:'1956年8月，上海徐家汇火车站欢送赴陕师生。',credit:'西安交大“西迁记忆”',url:'https://xqjy.xjtu.edu.cn/info/1063/1245.htm',sourceId:'S11'},
  opening:{file:'opening-1956.jpg',title:'课堂在西安继续',caption:'1956年9月10日，迁校后首次开学典礼。',credit:'西安交大“西迁记忆”',url:'https://xqjy.xjtu.edu.cn/info/1063/1246.htm',sourceId:'S8'},
  walk:{file:'walk-2026.png',title:'把来路走成新的出发',caption:'“重走长征路 奋进新征程”教职工健步走活动报道配图，活动于2026年4月10日启动。',credit:'西安交通大学新闻网；图片：校工会',url:'https://news.xjtu.edu.cn/info/1007/230870.htm',sourceId:'S13'},
};
