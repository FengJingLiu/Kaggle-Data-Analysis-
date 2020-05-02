# 酒店预订数据分析
## 加载库


```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
%matplotlib inline
```

## 数据加载及预览
### 列名解释
* **酒店类型** City Hotel-城市酒店 Resort Hotel-度假酒店
* **is_canceled** 预定是否取消 1-取消 0未取消
* **lead_time** 进入PMS（酒店物业管理系统）订房日期与到店日期间隔
* **arrival_date_year** 到店年份
* **arrival_date_month** 到店月份
* **arrival_date_week_number** 到店星期是一年中的第几个星期
* **arrival_date_day_of_month** 到店日期
* **stays_in_weekend_nights** 周末入住的夜数
* **stays_in_week_nights** 工作日入住的夜数
* **adults** 成年人数量
* **children** 孩子数量
* **babies** 婴儿数量
* **meal** 餐食规格 SC-未定义 BB-早餐 HB-早餐加中餐或午餐 BB-全餐
* **country** 来自哪个国家
* **market_segment** 细分市场名称 TO-旅游批发商 TA-旅游零售商
* **distribution_channel** 预定渠道
* **is_repeated_guest** 预定名是否来自于重复的客人 1为是 0为否
* **previous_cancellations** 客户在当前预定前取消预订的次数
* **previous_bookings_not_canceled** 客户在当前预定前未取消预订的次数
* **reserved_room_type** 预定房型
* **assigned_room_type** 分配房型（预定房型已满或其他原因）
* **booking_changes** 从预定到入住订单的修改次数
* **deposit_type** 押金类型 No Deposit0没有押金 Non Refund-押金不退还 Refundable-押金可退还
* **agent** 旅行社ID
* **company** 预定公司的ID
* **days_in_waiting_list** 订单确认前在等待列表中的天数
* **customer_type** 顾客类型 Contract-合同 Group-团体 Transient-临时 Transient-party-与其他临时订单相关
* **adr** 平均每晚入住花费
* **required_car_parking_spaces** 客户要求的停车位数量
* **total_of_special_requests** 特殊要求数量
* **reservation_status** 订单状态 Canceled-取消 Check-Out-已退房完成订单 No-Show-未入住
* **reservation_status_date** 设置订单最后状态的日期


```python
df = pd.read_csv('hotel_bookings.csv')
df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 119390 entries, 0 to 119389
    Data columns (total 32 columns):
     #   Column                          Non-Null Count   Dtype  
    ---  ------                          --------------   -----  
     0   hotel                           119390 non-null  object 
     1   is_canceled                     119390 non-null  int64  
     2   lead_time                       119390 non-null  int64  
     3   arrival_date_year               119390 non-null  int64  
     4   arrival_date_month              119390 non-null  object 
     5   arrival_date_week_number        119390 non-null  int64  
     6   arrival_date_day_of_month       119390 non-null  int64  
     7   stays_in_weekend_nights         119390 non-null  int64  
     8   stays_in_week_nights            119390 non-null  int64  
     9   adults                          119390 non-null  int64  
     10  children                        119386 non-null  float64
     11  babies                          119390 non-null  int64  
     12  meal                            119390 non-null  object 
     13  country                         118902 non-null  object 
     14  market_segment                  119390 non-null  object 
     15  distribution_channel            119390 non-null  object 
     16  is_repeated_guest               119390 non-null  int64  
     17  previous_cancellations          119390 non-null  int64  
     18  previous_bookings_not_canceled  119390 non-null  int64  
     19  reserved_room_type              119390 non-null  object 
     20  assigned_room_type              119390 non-null  object 
     21  booking_changes                 119390 non-null  int64  
     22  deposit_type                    119390 non-null  object 
     23  agent                           103050 non-null  float64
     24  company                         6797 non-null    float64
     25  days_in_waiting_list            119390 non-null  int64  
     26  customer_type                   119390 non-null  object 
     27  adr                             119390 non-null  float64
     28  required_car_parking_spaces     119390 non-null  int64  
     29  total_of_special_requests       119390 non-null  int64  
     30  reservation_status              119390 non-null  object 
     31  reservation_status_date         119390 non-null  object 
    dtypes: float64(4), int64(16), object(12)
    memory usage: 29.1+ MB
    

## 数据预处理
我们看到



```python
full_data_cln = pd.read_csv('hotel_bookings.csv')
full_data_cln.shape
full_data_cln.columns

# After cleaning, separate Resort and City hotel
# To know the acutal visitor numbers, only bookings that were not canceled are included. 
rh = full_data_cln.loc[(full_data_cln["hotel"] == "Resort Hotel") & (full_data_cln["is_canceled"] == 0)]
ch = full_data_cln.loc[(full_data_cln["hotel"] == "City Hotel") & (full_data_cln["is_canceled"] == 0)]


# get number of acutal guests by country
country_data = pd.DataFrame(full_data_cln.loc[full_data_cln["is_canceled"] == 0]["country"].value_counts())
#country_data.index.name = "country"
country_data.rename(columns={"country": "Number of Guests"}, inplace=True)
total_guests = country_data["Number of Guests"].sum()
country_data["Guests in %"] = round(country_data["Number of Guests"] / total_guests * 100, 2)
country_data["country"] = country_data.index
#country_data.loc[country_data["Guests in %"] < 2, "country"] = "Other"

# pie plot
fig = go.Figure()
fig = fig.add_trace(go.pie(country_data,
             values="Number of Guests",
             names="country",
             title="Home country of guests"
             ))
fig.update_traces(textposition="inside", textinfo="value+percent+label")
fig.show()


```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    <ipython-input-14-fc47e7e6bf5b> in <module>
         23              values="Number of Guests",
         24              names="country",
    ---> 25              title="Home country of guests"
         26              ))
         27 fig.update_traces(textposition="inside", textinfo="value+percent+label")
    

    TypeError: 'module' object is not callable



```python
N = 100
x = np.random.rand(N)
y = np.random.rand(N)
colors = np.random.rand(N)
sz = np.random.rand(N) * 30

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=x,
    y=y,
    mode="markers",
    marker=go.scatter.Marker(
        size=sz,
        color=colors,
        opacity=0.6,
        colorscale="Viridis"
    )
))

fig.show()
```


        <script type="text/javascript">
        window.PlotlyConfig = {MathJaxConfig: 'local'};
        if (window.MathJax) {MathJax.Hub.Config({SVG: {font: "STIX-Web"}});}
        if (typeof require !== 'undefined') {
        require.undef("plotly");
        define('plotly', function(require, exports, module) {
            /**
* plotly.js v1.53.0
* Copyright 2012-2020, Plotly, Inc.
* All rights reserved.
* Licensed under the MIT license
*/
        });
        require(['plotly'], function(Plotly) {
            window._Plotly = Plotly;
        });
        }
        </script>




<div>


            <div id="87555006-1fd5-40bd-86f5-1299e80e81f9" class="plotly-graph-div" style="height:525px; width:100%;"></div>
            <script type="text/javascript">
                require(["plotly"], function(Plotly) {
                    window.PLOTLYENV=window.PLOTLYENV || {};

                if (document.getElementById("87555006-1fd5-40bd-86f5-1299e80e81f9")) {
                    Plotly.newPlot(
                        '87555006-1fd5-40bd-86f5-1299e80e81f9',
                        [{"marker": {"color": [0.995889182271818, 0.6036511279348703, 0.19793821827372937, 0.4216917054055648, 0.20642087711046653, 0.735467054677009, 0.19654783646534857, 0.4941181613964766, 0.7419951018762095, 0.7296269158992942, 0.019458675397661218, 0.1363360827643264, 0.6190899419365617, 0.21308991426170854, 0.9780078385955236, 0.9526215034877812, 0.88851412045926, 0.8012812161045618, 0.2867812256615778, 0.4597573366967759, 0.4517264853778742, 0.34344168648804463, 0.9032617980114322, 0.5434201494989985, 0.44082222224823175, 0.715033082764684, 0.13289241948922348, 0.7171455903648807, 0.26138695441965765, 0.5245327267985249, 0.03646629881720942, 0.266938034196629, 0.10979117985047204, 0.3759532731555052, 0.17569489876124678, 0.834947468903623, 0.007913076198849733, 0.20115632841175435, 0.32517666390707334, 0.8541550016066692, 0.7151619388267585, 0.708000147046684, 0.4048784404717436, 0.12355498061469472, 0.7440126860801048, 0.08162942445811083, 0.8012357529314116, 0.4087976302804759, 0.7858103788236496, 0.6936948616127235, 0.3596599548793159, 0.3780388728080464, 0.4704468040430242, 0.5133530755731087, 0.9760639941047696, 0.30864629508738217, 0.4096361760690328, 0.35228701133856066, 0.2516574402690419, 0.7620968366579631, 0.6797250694793163, 0.6404150363232844, 0.7115144211813826, 0.09000482402543153, 0.6766683416915504, 0.5163207242573083, 0.5495304895512934, 0.956987354008142, 0.479003453760514, 0.7017782766846339, 0.6123506089054908, 0.27556614296600546, 0.5824452822737927, 0.4444597312352879, 0.19155082648168298, 0.31826937097793195, 0.8771067047158537, 0.25766408577957534, 0.6579935114597433, 0.06811191885417311, 0.0827606754147776, 0.948613404692992, 0.2530073485255251, 0.2719129174685462, 0.5404380510281769, 0.5271927406759374, 0.4206522103474438, 0.22572872106569564, 0.7903250178875518, 0.4894968843730605, 0.4191468128727903, 0.3183663213023329, 0.36822947112433313, 0.8073339442212167, 0.7318237735956274, 0.9881126840980824, 0.7662816498040695, 0.034621577113480906, 0.31353261013473266, 0.008018825862041168], "colorscale": [[0.0, "#440154"], [0.1111111111111111, "#482878"], [0.2222222222222222, "#3e4989"], [0.3333333333333333, "#31688e"], [0.4444444444444444, "#26828e"], [0.5555555555555556, "#1f9e89"], [0.6666666666666666, "#35b779"], [0.7777777777777778, "#6ece58"], [0.8888888888888888, "#b5de2b"], [1.0, "#fde725"]], "opacity": 0.6, "size": [10.154729995508756, 22.322826761666043, 9.12743688842304, 14.390716148716473, 10.153139299929066, 6.752473723290704, 25.385830232118717, 11.021367019845322, 8.552512128855577, 28.588991427265725, 26.151745904856035, 28.999073244178014, 9.697898479278825, 26.02583708935449, 22.282605200506875, 4.726015692254042, 13.159653211359808, 2.515814886174871, 26.058895993082707, 25.381764400228725, 22.48236720693192, 4.841311657535242, 23.941120765423246, 14.694071939215934, 19.386705539858088, 4.820745228025185, 15.77774753663602, 3.688513994292275, 2.6302683748515756, 9.871773891314803, 17.39801616518171, 12.070910973056595, 12.427663943317732, 19.312752007961045, 23.55991276236214, 12.621371606213463, 4.608526234219329, 25.753681795171193, 22.015167716059107, 26.2142824723751, 20.584874539603405, 18.218627913671718, 26.16860010953619, 15.405311659672368, 15.91087040349899, 1.7221192661723117, 17.403847230119876, 9.424636826710143, 3.8856685208526374, 25.710525820784266, 17.634824793549917, 4.085864838299251, 14.337395450625328, 1.6507400337845335, 8.078876119634025, 12.510568150528202, 1.502839234857083, 0.7668432402885672, 25.026812419557523, 19.075892709111407, 2.3667746917776933, 16.209719964792562, 28.8375029958667, 10.385098328757184, 26.35197319117594, 8.96889479040281, 11.040859161973675, 16.424805790496354, 1.145023316083581, 12.018605428237295, 20.403897333229235, 23.608521889175865, 11.877612872047386, 2.3788319320916274, 11.133116831741187, 8.110774135978824, 13.294307201021459, 11.698850725923847, 4.726911490344381, 6.356518559168358, 24.661889645847197, 13.87054752041554, 11.390582095896573, 14.842964568245907, 22.05307435497466, 24.310949286337042, 18.22254497807523, 10.870652067337135, 29.1701705790649, 3.3876327014487497, 12.830876255257616, 29.799474155575947, 11.541022441869996, 27.6271935482396, 10.579441621885508, 19.451990637803377, 11.322944272831016, 13.754792259439427, 1.6524287486812395, 10.430802266917137]}, "mode": "markers", "type": "scatter", "x": [0.7517444676019522, 0.43259071195340215, 0.6810645172836822, 0.8437565688419392, 0.8453567766379448, 0.2527232095412637, 0.10816522695871711, 0.9438807543034169, 0.3145139549460637, 0.6397902821956624, 0.7786964309500964, 0.09863695256773686, 0.9959643289893776, 0.6251816753056132, 0.4914310272739285, 0.025062031326109624, 0.460384931676621, 0.07641037818195573, 0.12956994893040363, 0.14574009959111212, 0.49758200645785533, 0.6248676681831645, 0.4985538156645283, 0.8200394013425002, 0.2997633296222004, 0.4789446482589058, 0.17697009590562063, 0.1823499908725743, 0.7671451802901779, 0.47349703246735697, 0.5167777489189965, 0.5468118684327151, 0.8806726078329709, 0.893889118050917, 0.009501095586843533, 0.3732917309499342, 0.3835280919505947, 0.3707225980353025, 0.7550688349962702, 0.7175772194326262, 0.5292989932504074, 0.8580413098295643, 0.48270399994118074, 0.00048226497637293697, 0.45314761149298266, 0.2640660419693307, 0.5760225500433309, 0.874770334170628, 0.5945975850857446, 0.29195788293151226, 0.6468007391588839, 0.3594764573185625, 0.259589172172608, 0.7829500109606825, 0.8683419269401977, 0.5611489612336417, 0.7700501957033334, 0.20399014779248603, 0.11717513318590111, 0.43473007779158934, 0.4694029521388421, 0.03143005480344008, 0.4534951652064274, 0.7990609653973508, 0.7646301683647635, 0.8627104235750584, 0.6206321024739555, 0.4934238864948667, 0.00642238911074855, 0.9999749870265138, 0.12415469411312641, 0.37571782087253636, 0.7838740081808095, 0.010531370909728222, 0.32258132388943006, 0.10263307096848517, 0.16569403516563486, 0.710472825495166, 0.43322845333011084, 0.6319611909582509, 0.6283370897701993, 0.261899889680284, 0.7369992033503875, 0.9252180321716557, 0.28726407863476777, 0.6550498798108408, 0.5516918889107295, 0.03892903108874768, 0.1923505062472679, 0.858600082059914, 0.24307789756106268, 0.5082562435037634, 0.6777601967351763, 0.40704791661622075, 0.4226705490630338, 0.3893706617028617, 0.11860331269315982, 0.004930092261732244, 0.4881295602131752, 0.7269120821257279], "y": [0.3815691876932614, 0.2736558094317284, 0.30557704016363774, 0.809249554843655, 0.9240629001033135, 0.7794131109413994, 0.9535179440907021, 0.4483627426634712, 0.4098515539034505, 0.8947773081634282, 0.8041267531195593, 0.2657699861511922, 0.8987512425166924, 0.053344251217855354, 0.8512810826059303, 0.9692087977038512, 0.9530817977964473, 0.18837880871399937, 0.12739007785660372, 0.6290719173068638, 0.935384832557778, 0.8816504518776562, 0.9143152838374815, 0.0342712710885803, 0.28243262949894654, 0.6861997643231604, 0.8803350181693121, 0.7012730138864428, 0.32728968278099013, 0.5443402419553622, 0.38200267275698474, 0.6808935676349587, 0.3575597721996945, 0.38323718373501925, 0.32841654243696106, 0.7184624167285176, 0.3449133384010077, 0.9305870382659316, 0.8080345847101291, 0.4006323457999592, 0.3722508074710804, 0.9156875998375683, 0.10276220497105526, 0.0631650558334087, 0.05517539040342845, 0.03651683701435604, 0.2878904741299295, 0.08222847821198676, 0.4160280424263032, 0.9864370186758356, 0.1571830000751302, 0.8165960882925059, 0.48249179533491315, 0.2041892605011777, 0.5243704052879876, 0.933002055865703, 0.3550625543538457, 0.6634385980352869, 0.3450699262000234, 0.9656694711359894, 0.7176370020645859, 0.01111492891814736, 0.4667532621698318, 0.1512908536297951, 0.7167216887654944, 0.2850676050402431, 0.8926629512749374, 0.9233472969221488, 0.9792151868981359, 0.006637352372217631, 0.5996671983120165, 0.15500926589027875, 0.9692240546715595, 0.6324772274334709, 0.05381443207479997, 0.5998007680511966, 0.6587155868251279, 0.885243892640579, 0.23789665792520664, 0.536791421972864, 0.8652367397638321, 0.2774531941109589, 0.26512281912759406, 0.25258908967548455, 0.609333205270958, 0.5980486376489373, 0.7271885929786055, 0.7640788632034842, 0.5529364047523121, 0.7697513656571388, 0.6395955061828934, 0.1842153625446462, 0.4728347464081679, 0.4905489820935578, 0.7422039102680394, 0.24022240055859945, 0.7765113296868897, 0.3843799629961693, 0.255090859438288, 0.9845717837161398]}],
                        {"template": {"data": {"bar": [{"error_x": {"color": "#2a3f5f"}, "error_y": {"color": "#2a3f5f"}, "marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "bar"}], "barpolar": [{"marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "barpolar"}], "carpet": [{"aaxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "baxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "type": "carpet"}], "choropleth": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "choropleth"}], "contour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "contour"}], "contourcarpet": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "contourcarpet"}], "heatmap": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmap"}], "heatmapgl": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmapgl"}], "histogram": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "histogram"}], "histogram2d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2d"}], "histogram2dcontour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2dcontour"}], "mesh3d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "mesh3d"}], "parcoords": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "parcoords"}], "pie": [{"automargin": true, "type": "pie"}], "scatter": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter"}], "scatter3d": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter3d"}], "scattercarpet": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattercarpet"}], "scattergeo": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergeo"}], "scattergl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergl"}], "scattermapbox": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattermapbox"}], "scatterpolar": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolar"}], "scatterpolargl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolargl"}], "scatterternary": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterternary"}], "surface": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "surface"}], "table": [{"cells": {"fill": {"color": "#EBF0F8"}, "line": {"color": "white"}}, "header": {"fill": {"color": "#C8D4E3"}, "line": {"color": "white"}}, "type": "table"}]}, "layout": {"annotationdefaults": {"arrowcolor": "#2a3f5f", "arrowhead": 0, "arrowwidth": 1}, "coloraxis": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "colorscale": {"diverging": [[0, "#8e0152"], [0.1, "#c51b7d"], [0.2, "#de77ae"], [0.3, "#f1b6da"], [0.4, "#fde0ef"], [0.5, "#f7f7f7"], [0.6, "#e6f5d0"], [0.7, "#b8e186"], [0.8, "#7fbc41"], [0.9, "#4d9221"], [1, "#276419"]], "sequential": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "sequentialminus": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]}, "colorway": ["#636efa", "#EF553B", "#00cc96", "#ab63fa", "#FFA15A", "#19d3f3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"], "font": {"color": "#2a3f5f"}, "geo": {"bgcolor": "white", "lakecolor": "white", "landcolor": "#E5ECF6", "showlakes": true, "showland": true, "subunitcolor": "white"}, "hoverlabel": {"align": "left"}, "hovermode": "closest", "mapbox": {"style": "light"}, "paper_bgcolor": "white", "plot_bgcolor": "#E5ECF6", "polar": {"angularaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "radialaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "scene": {"xaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "yaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "zaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}}, "shapedefaults": {"line": {"color": "#2a3f5f"}}, "ternary": {"aaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "baxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "caxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "title": {"x": 0.05}, "xaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}, "yaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}}}},
                        {"responsive": true}
                    ).then(function(){

var gd = document.getElementById('87555006-1fd5-40bd-86f5-1299e80e81f9');
var x = new MutationObserver(function (mutations, observer) {{
        var display = window.getComputedStyle(gd).display;
        if (!display || display === 'none') {{
            console.log([gd, 'removed!']);
            Plotly.purge(gd);
            observer.disconnect();
        }}
}});

// Listen for the removal of the full notebook cells
var notebookContainer = gd.closest('#notebook-container');
if (notebookContainer) {{
    x.observe(notebookContainer, {childList: true});
}}

// Listen for the clearing of the current output cell
var outputEl = gd.closest('.output');
if (outputEl) {{
    x.observe(outputEl, {childList: true});
}}

                        })
                };
                });
            </script>
        </div>



```python

```