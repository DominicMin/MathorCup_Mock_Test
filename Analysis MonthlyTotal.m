clear;
T=readtable("附件1：物流网络历史货量数据.xlsx","VariableNamingRule","preserve");
x=T(strcmp(T.("场地1"),"DC14"),:);
y=x(strcmp(x.("场地2"),"DC10"),:);
days=[31 28 31 30 31 30 31 31 30 31 30 31];
sum=0;
num=[];
for month=1:12
    for i=1:days(month)
        index=find(y.("日期")==sprintf("%s%d%s%d","2021-0",month,"-0",i));
        if index==[]
            continue;
        end
        sum=sum+y.("货量")(index);
    end
    num=[num,sum];
    sum=0;
end
for month=1:12
    for i=1:days(month)
        index=find(y.("日期")==sprintf("%s%d%s%d","2022-0",month,"-0",i));
        sum=sum+y.("货量")(index);
    end
    num=[num,sum];
    sum=0;
end
bar(num);
set(gca,"YScale","log");