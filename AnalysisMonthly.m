tiledlayout(5,6);
title("DC14-DC10");
T=readtable("附件1：物流网络历史货量数据.xlsx","VariableNamingRule","preserve");
x=T(strcmp(T.("场地1"),"DC14"),:);
y=x(strcmp(x.("场地2"),"DC10"),:);
t=size(y,1);
for a=1:30:t
    if(a+30>t)
        nexttile;
        bar(y.("货量")(a:t));
        set(gca,"YScale","log");
        title(sprintf("%s %d","month",int64(a/30+1)));
    else
        nexttile;
        bar(y.("货量")(a:a+30));
        set(gca,"YScale","log" );
        title(sprintf("%s %d","month",int64(a/30+1)));
    end
end
