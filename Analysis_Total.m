clear;
tiledlayout(2,2);
nexttile([1,2]);
T=readtable("附件1：物流网络历史货量数据.xlsx","VariableNamingRule","preserve");
days=[31 28 31 30 31 30 31 31 30 31 30 31];
total=[];
for i=1:12
    for j=1:days(i)
        if j<=9
            index=find(T.("日期")==sprintf("2021-0%d-0%d",i,j));
        else
            index=find(T.("日期")==sprintf("2021-0%d-%d",i,j));
        end
        total=[total,sum(T.("货量")(index))];
    end
end
bar(total);
set(gca,"YScale","log");
nexttile([1,2]);
total=[];
for i=1:12
    for j=1:days(i)
        if j<=9
            index=find(T.("日期")==sprintf("2022-0%d-0%d",i,j));
        else
            index=find(T.("日期")==sprintf("2022-0%d-%d",i,j));
        end
        total=[total,sum(T.("货量")(index))];
    end
end
bar(total);
set(gca,"YScale","log");