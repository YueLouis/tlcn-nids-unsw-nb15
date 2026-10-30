"""Generate the remaining planned tables/plots from validated frozen diagnostics."""
from pathlib import Path
import json
import shutil

import pandas as pd

from prepare_dot3_draft import table, pm

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'docs/evidence/dot_03/final_diagnostics_20261025'


def tex(value):
    return str(value).replace('_',r'\_').replace('%',r'\%').replace('&',r'\&')


def figure(name,caption,width='.98'):
    return '\n'+r'\begin{figure}[H]\centering'+'\n'+rf'\includegraphics[width={width}\textwidth]{{assets/final_diagnostics/{name}.png}}'+'\n'+r'\caption{'+caption+r'}\end{figure}'+'\n'


def prepare():
    audit=json.loads((DATA/'FINAL_DIAGNOSTICS_AUDIT.json').read_text(encoding='utf-8'))
    assert audit['run_count']==80 and audit['metric_checks']==1040 and audit['inputs_unchanged']
    project=ROOT/'docs/report_dot3_20261025'
    assets=project/'assets/final_diagnostics';assets.mkdir(parents=True,exist_ok=True)
    for path in DATA.glob('*.png'):shutil.copy2(path,assets/path.name)
    groups=pd.read_csv(DATA/'GROUP_ERRORS_MEAN_STD.csv',float_precision='round_trip')
    costs=pd.read_csv(DATA/'RUNTIME_SIZE_MEAN_STD.csv',float_precision='round_trip')
    stability=pd.read_csv(DATA/'ERROR_STABILITY.csv',float_precision='round_trip')
    pairs=pd.read_csv(DATA/'MODEL_DISAGREEMENT_S42.csv',float_precision='round_trip')
    near=pd.read_csv(DATA/'NEAR_THRESHOLD_EXAMPLES_S42.csv',float_precision='round_trip')
    hardware=json.loads((DATA/'HARDWARE_CURRENT.json').read_text(encoding='utf-8'))
    rows=[]
    for scenario,role in [('CS','normal'),('LR','heldout_attack')]:
        for model in ('RF','IF'):
            for dimension in ('proto','service','state'):
                p=groups[(groups.scenario==scenario)&(groups.model==model)&(groups.target_fpr==.05)&(groups.evaluation_role==role)&(groups.dimension==dimension)&(groups.support_min>=100)].sort_values(['error_rate_mean','feature_value'],ascending=[False,True]).head(1)
                for r in p.itertuples():rows.append([scenario,model,dimension,tex(r.feature_value),f'{int(r.support_min):,}',pm(r.error_rate_mean,r.error_rate_std,True)])
    slices_table=table('Lát cắt lỗi thăm dò tại target validation 5\\%; mean/sample std năm seed; tỷ lệ lỗi theo \\%, std theo điểm phần trăm',
        'Sc. & Model & Chiều & Giá trị & Support & Tỷ lệ lỗi', 'L{.6cm}L{1.1cm}L{1.4cm}L{3.3cm}rL{3.4cm}',rows)
    rows=[]
    for scenario in ('CS','LR','LD','LE'):
        for model in ('RF','XGB','IF','AE'):
            p=stability[(stability.scenario==scenario)&(stability.model==model)&(stability.target_fpr==.05)]
            vals=[]
            for role in ('normal','heldout_attack'):
                q=p[p.evaluation_role==role]
                vals.append('--' if q.empty else f'{int(q.loc[q.error_seed_count==5,"record_count"].iloc[0]):,} / {int(q.role_support.iloc[0]):,}')
            rows.append([scenario,model,*vals])
    stability_table=table('Record sai ở cả năm seed tại target validation 5\\%; cùng official test; không là năm test độc lập',
        'Sc. & Model & Normal sai 5/5 / support & Held-out sai 5/5 / support','L{1cm}L{1.1cm}L{5.2cm}L{5.2cm}',rows)
    rows=[]
    for r in pairs[(pairs.target_fpr==.05)&pairs.scenario.isin(['CS','LR'])].itertuples():
        rows.append([r.scenario,r.model_a+' / '+r.model_b,f'{r.different_prediction_count:,}',f'{r.both_wrong:,}',f'{r.error_jaccard:.4f}'])
    pairs_table=table('Bất đồng và giao lỗi giữa model, seed 42, target validation 5\\%, cùng 82.332 record',
        'Sc. & Cặp model & Khác dự đoán & Cùng sai & Jaccard lỗi','L{.7cm}L{2.1cm}rrr',rows)
    rows=[]
    selected=near[(near.run_id.isin(['LR-RF-S42','LR-IF-S42']))&(near.target_fpr==.05)&near.evaluation_role.isin(['normal','heldout_attack'])].sort_values(['run_id','evaluation_role','abs_margin','record_id']).groupby(['run_id','evaluation_role'],sort=True).head(1)
    for r in selected.itertuples():
        outcome=('TP' if r.y_pred else 'FN') if r.y_true else ('FP' if r.y_pred else 'TN')
        rows.append([r.run_id.split('-')[1],str(r.record_id),outcome,f'{r.abs_margin:.2g}',tex(r.proto),tex(r.service),f'{r.dur:.3g}',str(int(r.sttl)),str(int(r.dbytes))])
    near_table=table('Ví dụ gần ngưỡng nhất theo model/vai trò: LR seed 42, target validation 5\\%; số học chỉ dùng mô tả',
        'Model & ID & KQ & $|s-\\tau|$ & proto & service & dur (s) & sttl & dbytes','L{1.1cm}rL{.6cm}rL{.9cm}L{1.2cm}rrr',rows)
    rows=[]
    for scenario in ('CS','LR','LD','LE'):
        for model in ('RF','XGB','IF','AE'):
            r=costs[(costs.scenario==scenario)&(costs.model==model)].iloc[0]
            rows.append([scenario,model,pm(r.total_run_seconds_mean,r.total_run_seconds_std),pm(r.current_inference_ms_mean,r.current_inference_ms_std),pm(r.bundle_mb_mean,r.bundle_mb_std)])
    costs_table=table('Chi phí mô tả, mean/sample std qua năm seed; tổng run lịch sử khác phép đo suy luận hiện tại',
        'Sc. & Model & Tổng run cũ (s) & Suy luận 100 dòng (ms) & Bundle (MB)',
        'L{.6cm}L{1cm}L{3.5cm}L{4.5cm}L{3cm}',rows)
    text=r'''
\section{Đọc trade-off, ma trận lỗi và độ ổn định}
Phần này hoàn tất bộ hình dự kiến từ prediction đã khóa. Hai target 1\%/5\% do validation quyết định; trục FPR trong hình trade-off là FPR quan sát trên test. Mean/sample std dùng năm seed trên cùng official test, không phải khoảng tin cậy hoặc bằng chứng tổng quát ra hệ thống vận hành. CS không có held-out nên không vẽ UADR CS. Ma trận dùng seed 42 đã định trước, không chọn seed có kết quả đẹp.
'''
    text+=figure('UADR_BOTH_TARGETS','UADR theo ba lớp held-out ở hai target validation; mean/sample std qua năm seed, mô phỏng giấu lớp.')
    text+=figure('TRADEOFF_KNOWN_RECALL','Known Attack Recall theo FPR test quan sát; hai điểm là target validation 1\\%/5\\%, mean/sample std năm seed.')
    text+=figure('TRADEOFF_UADR','UADR theo FPR test quan sát; ba LOACO, mean/sample std năm seed. Đọc đồng thời khả năng bắt held-out và báo nhầm.')
    text+=figure('CONFUSION_ALL_SCENARIOS_S42','Ma trận nhầm lẫn cho CS và ba LOACO, bốn model, seed 42, target validation 5\\%. Hàng là nhãn thật, cột là dự đoán.','.94')
    text+=figure('CATEGORY_DETECTION_HEATMAP','Detection rate từng attack category, target validation 5\\%; mean năm seed; support đầy đủ trong CSV category.','.94')
    text+=figure('SEED_STABILITY','Độ biến thiên theo seed trên cùng test. CS dùng recall Attack; LOACO dùng UADR; target validation 5\\%.')
    text+='\n'+r'\begin{figure}[H]\centering\includegraphics[width=.92\textwidth]{assets/dot3_20261025/PR_CS_all_S42.png}\caption{PR closed-set cho bốn model, seed 42; AP dùng một score mỗi record, hai target chỉ xác định điểm vận hành.}\end{figure}'+'\n'
    for scenario,title in [('LD','DoS'),('LE','Exploits')]:
        text+='\n'+rf'\begin{{figure}}[H]\centering\includegraphics[width=.96\textwidth]{{assets/dot3_20261025/SCORE_ECDF_{scenario}_S42.png}}\caption{{ECDF score LOACO {title}, seed 42; Normal, known Attack, held-out và hai threshold validation.}}\end{{figure}}'+'\n'
    text+=r'''
\section{Lỗi theo protocol, service và state}
Đặc tả \path{docs/management/DAC_TA_CHAN_DOAN_CUOI_20261025.md} ghi quy tắc trước chạy. Ghép từng prediction về raw official test theo ID, kiểm nhãn/category/role và đủ hai target; 80 run, 13.173.120 dòng prediction và 1.040 metric gốc tiếp tục khớp. Với mỗi giá trị proto/service/state, tính support và TP/FP/TN/FN riêng theo Normal, known Attack, held-out Attack. Ở Normal, tỷ lệ lỗi là FP/support; ở Attack là FN/support. Không cộng ba chiều rồi coi là số record độc lập.

Bảng sau chọn một giá trị có tỷ lệ lỗi mean cao nhất trong mỗi chiều, model và scope, chỉ trong nhóm support ít nhất 100. Hình giữ tối đa sáu nhóm cùng quy tắc. Đây là chọn để thăm dò lỗi trong test đang có, không kiểm định giả thuyết mới, không ước lượng nhân quả, không đại diện nhóm ít mẫu bị lược khỏi hình. CSV giữ toàn bộ nhóm và cả target 1\%/5\%; support của nhóm không thay giữa seed trong cùng role/scenario.
'''+slices_table
    text+=figure('FP_GROUPS_CS','Lỗi Normal closed-set (FP), RF/IF, target validation 5\\%; nhóm support tối thiểu 100, chọn tối đa sáu tỷ lệ cao nhất, mean/sample std năm seed.','.93')
    text+=figure('FN_GROUPS_LR','Lỗi held-out Reconnaissance (FN), RF/IF, target validation 5\\%; cùng quy tắc support và chọn nhóm, mean/sample std năm seed.','.93')
    text+=r'''
Tỷ lệ lỗi cao trong một service/protocol có thể đi kèm loại Attack, phân bố feature và dữ liệu gần giống nhau. Bảng này định vị chỗ cần đọc lại, không chứng minh service hoặc protocol gây lỗi. Khi trao đổi, Thu cần nêu đúng role, giá trị nhóm, support và target trước khi nói phần trăm; Anh kiểm giới hạn của phép ghép và nguồn dữ liệu.

\section{Ví dụ sát ngưỡng, lỗi lặp và bất đồng model}
Mỗi model seed 42, target và role lấy ba record có $|score-threshold|$ nhỏ nhất, hòa thì ID nhỏ trước. Bảng minh họa dưới chỉ lấy record gần nhất ở LR/RF và LR/IF cho Normal/held-out; có cả dự đoán đúng và sai, không chọn riêng trường hợp thuận lợi. dur, sttl, dbytes là feature raw để mở lại dòng gốc. Khoảng cách score chỉ đọc trong cùng model; không so khoảng cách RF với IF để nói model nào tự tin hơn. Feature importance toàn model ở phần trước không giải thích nguyên nhân từng dòng này.
'''+near_table+stability_table
    text+=r'''
CSV \path{ERROR_STABILITY.csv} giữ đủ phân bố sai 0--5 seed cho mỗi role, model, scenario và target. Record sai cả năm seed cho thấy lỗi không biến mất chỉ bằng đổi seed trên test này; không kết luận lỗi bất khả kháng hoặc do một feature cụ thể. Hai model có cùng tỷ lệ tổng vẫn có thể sai ở các record khác nhau. Bảng cặp model ghi số dự đoán khác, số cùng sai và Jaccard của tập lỗi ($|A\cap B|/|A\cup B|$); chưa triển khai ensemble hoặc khẳng định gộp model sẽ tốt hơn.
'''+pairs_table
    text+=r'''
\section{Thời gian, kích thước artifact và phần chưa có bằng chứng lịch sử}
Metadata 80 run có \texttt{duration\_seconds} của toàn run. Không có log tách riêng thời gian train, suy luận cũ hoặc cấu hình phần cứng huấn luyện. Vì vậy cột tổng run dưới đây không được gọi là thời gian train; trường train-only trong CSV để thiếu. Không huấn luyện lại để tạo giả một phép đo lịch sử.

Phép đo mới ngày 25/10 dùng đủ 80 bundle đã lưu, cùng 100 dòng mẫu demo được chọn trước, một lượt warm-up và ba lượt transform+score mỗi bundle. Không gồm load bundle, HTTP, I/O hay khởi động Python. Mean trong bảng là mean qua năm seed của mean ba lượt; std là sample std qua seed; CSV còn giữ std ba lượt từng bundle. Mỗi bundle được đối chiếu score và prediction với dữ liệu khóa, tổng 8.000 score, dung sai $10^{-6}$; không sửa threshold. MB là $10^6$ byte, gồm cả preprocessor và estimator.
'''+costs_table
    text+='\nMáy đo suy luận hiện tại: '+tex(hardware.get('cpu_name',hardware['processor']))+f", {hardware['logical_cpus']} logical CPU, Python 3.14.4; cấu hình hệ điều hành chi tiết ở "+r'\path{HARDWARE_CURRENT.json}.'+' Đây là thông tin máy đo hiện tại, không xác nhận máy của các run lịch sử. Thời gian trên mẫu nhỏ chịu cache, tải máy và mức song song mặc định; không dùng để kết luận độ trễ live, throughput vận hành hoặc so chi phí train công bằng.\n'
    text+=r'''
\section{Đối chiếu phạm vi hoàn tất kỹ thuật}
Bộ mới bổ sung các bảng T9/T10 và các hình còn thiếu của kế hoạch. T9 vẫn thiếu bằng chứng thời gian train riêng và phần cứng lịch sử; báo cáo nêu đúng khoảng trống này. Các hình PR closed-set và ECDF từng LOACO, importance đủ scenario nằm trong bộ asset và CSV đi kèm; các hình chính được đưa vào bản đọc. Prototype bản đợt 4 có cùng CSV qua bốn model và giải thích score/feature phù hợp. Các bước này hoàn tất phần chuẩn bị phân tích, không xác nhận việc thành viên đã đọc, tự chạy hoặc giảng viên đã duyệt.

Nguồn chính: \path{docs/evidence/dot_03/final_diagnostics_20261025/}; audit có hash bốn artifact mỗi run, kiểm raw và đối chiếu metric. Nguồn S07 vẫn chỉ sử dụng abstract đã đối chiếu, không viện dẫn kết quả toàn văn chưa đọc. Bản nộp cần cả nhóm xem, sửa, tự giải thích và quyết định dùng nội dung nào.
'''
    (project/'final_diagnostics.tex').write_text(text,encoding='utf-8')
    print('Prepared final diagnostic tables/figures chapter from 80 validated runs.')


if __name__=='__main__':prepare()
