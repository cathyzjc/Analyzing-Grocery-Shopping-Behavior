use db_consumer_panel;
show tables;
-- a How many:
-- Store shopping trips are recorded in your database?
select count(TC_id) from dta_at_TC;
-- Households appear in your database?
select count(hh_id) from dta_at_hh;
-- Stores of different retailers appear in our data base?
select count( distinct TC_retailer_code_store_code) from dta_at_TC;
-- Different products are recorded?
select count(prod_id) from dta_at_prod_id;
   -- i. Products per category and products per module
      select group_at_prod_id,count(prod_id) from dta_at_prod_id
      group by group_at_prod_id;
      select module_at_prod_id,count(prod_id) from dta_at_prod_id
      group by module_at_prod_id;
   -- ii. Plot the distribution of products and modules per department
	  select department_at_prod_id,count(distinct prod_id),count(distinct module_at_prod_id)
      FROM dta_at_prod_id group by department_at_prod_id;
-- Transactions?
   -- i. Total transactions and transactions realized under some kind of promotion.
      select count(*) from dta_at_TC_upc;
      select count(*) from dta_at_TC_upc
      where coupon_value_at_TC_prod_id <>0;

-- b Aggregate the data at the household‐monthly level to answer the following questions:
-- How many households do not shop at least once on a 3 month periods.
    
    DROP TABLE IF EXISTS TC_month1;
     CREATE TABLE TC_month1
	   SELECT hh_id, str_to_date(TC_date, '%Y-%m-%d') as date1, ROW_NUMBER() OVER (ORDER BY hh_id, str_to_date(TC_date, '%Y-%m-%d')) AS ID  FROM dta_at_TC
       order by ID;
       
     DROP TABLE IF EXISTS TC_month2;
     CREATE TABLE TC_month2
	   SELECT *, 1 + ID AS ID_2 FROM TC_month1 
       order by ID_2;
	
     DROP TABLE IF EXISTS TC_month;
     CREATE TABLE TC_month
	 SELECT    A.date1       as first_date  , 
			   B.date1       as second_date , 
               A.hh_id       as household,
          datediff(A.date1  , B.date1) AS TIME_WINDOW_SIZE
	 FROM    
	 TC_month1 AS A
	 INNER  JOIN
	 TC_month2 AS B
	 ON     A.ID = B.ID_2 and A.hh_id = B.hh_id
     where datediff(A.date1  , B.date1) > 90;
     select * from TC_month;
     select count(distinct household) from TC_month;

     -- i. Is it reasonable?
     -- ii. Why do you think this is occurring?
	 #  We think it is reasonable because customers may choose other platform to go shopping. For example, there is a new platform which promotes quite a lot so customers will prefer the new one.

-- Loyalism: Among the households who shop at least once a month, which % of them concentrate at least 80% of their grocery expenditure (on average) on single retailer? And among 2 retailers?
     DROP TABLE IF EXISTS TC_loyalism1;
     CREATE TABLE TC_loyalism1
	   SELECT hh_id, str_to_date(TC_date, '%Y-%m-%d') as date2, TC_total_spent, TC_retailer_code, ROW_NUMBER() OVER (ORDER BY hh_id, str_to_date(TC_date, '%Y-%m-%d')) AS ID  FROM dta_at_TC
       order by ID;
       
     DROP TABLE IF EXISTS TC_loyalism2;
     CREATE TABLE TC_loyalism2
	   SELECT *, 1 + ID AS ID_2 FROM TC_loyalism1
       order by ID_2;
    
    DROP TABLE IF EXISTS TC_loyalism;
     CREATE TABLE TC_loyalism
	 SELECT    A.date2     as first_date  , 
			   B.date2     as second_date , 
               A.hh_id       as household,
               A.TC_total_spent as grocery_expenditure,
               A.TC_retailer_code as retailer,
          datediff(A.date2  , B.date2) AS TIME_WINDOW_SIZE
	 FROM    
	 TC_loyalism1 AS A
	 INNER  JOIN
	 TC_loyalism2 AS B
	 ON     A.ID = B.ID_2 and A.hh_id = B.hh_id
     where datediff(A.date2  , B.date2) <= 30;
     select * from TC_loyalism;
  
     DROP TABLE IF EXISTS total_expenditure;
     CREATE TABLE total_expenditure
     select sum(grocery_expenditure) as total_expenditure, household
     from TC_loyalism
     group by household;
     select * from total_expenditure;
     
     # one retailer
     DROP TABLE IF EXISTS retail_expenditure;
     CREATE TABLE retail_expenditure
     select sum(grocery_expenditure) as retail_expenditure, household, retailer
     from TC_loyalism
     group by household, retailer;
     select * from retail_expenditure;
     
     DROP TABLE IF EXISTS expenditure1;
     CREATE TABLE expenditure1
     select A.total_expenditure, B.* 
     from total_expenditure as A
     right join retail_expenditure as B
     on A.household = B.household
     where B.retail_expenditure/A.total_expenditure >= 0.8;
     select count( distinct household) from expenditure1;
     
     # two retailers
	 DROP TABLE IF EXISTS retail2_expenditure;
     CREATE TABLE retail2_expenditure
     select retail_expenditure.*, ROW_NUMBER() OVER (partition by household ORDER BY retail_expenditure desc) AS ID from retail_expenditure;
     select * from retail2_expenditure;
     
	 DROP TABLE IF EXISTS retail_top_expenditure;
     CREATE TABLE retail_top_expenditure
     select sum(retail_expenditure) as retail2_expenditure, household from retail2_expenditure
     where ID = 1 Or ID = 2
     group by household;
     
	 DROP TABLE IF EXISTS expenditure2;
     CREATE TABLE expenditure2
     select A.total_expenditure, B.* 
     from total_expenditure as A
     right join retail_top_expenditure as B
     on A.household = B.household
     where B.retail2_expenditure/A.total_expenditure >= 0.8;
     select count(distinct household) from expenditure2;
     
     -- i. Are their demographics remarkably different? Are these people richer? Poorer?
     -- demographics distribution
     # one retailer
     SELECT hh_race, count(hh_id) from dta_at_hh,expenditure1
     WHERE dta_at_hh.hh_id=expenditure1.household
     group by hh_race;
     # two retailers
     SELECT hh_race, count(hh_id) from dta_at_hh,expenditure2
     WHERE dta_at_hh.hh_id=expenditure2.household
     group by hh_race;
	 -- From these two groups of distribution, we can see that they are remakably different. White Caucasian people are simply larger than the other two groups: African American and Asian.
     
     -- income distribution
     # one retailer
	 SELECT avg(hh_income) as group_income1, (select avg(hh_income) from dta_at_hh) as total_income 
     from dta_at_hh,expenditure1
     WHERE dta_at_hh.hh_id=expenditure1.household;
     # two retailer
	 SELECT avg(hh_income) as group_income2, (select avg(hh_income) from dta_at_hh) as total_income 
     from dta_at_hh,expenditure2
     WHERE dta_at_hh.hh_id=expenditure2.household;
     -- From these two groups of comparison, we can see that they are poorer than total household average.(17.3118/17.3367<18.717)
     
     -- ii. What is the retailer that has more loyalists?
     # one retailer
     SELECT retailer, count(household) as loyalist from expenditure1
     group by retailer
     order by count(household) desc limit 1;
     
     # two retailers
     drop table if exists loyalist;
     create table loyalist
     select retail2_expenditure.household, retail2_expenditure.retailer 
     from retail2_expenditure, expenditure2
     where retail2_expenditure.household = expenditure2.household
     and (retail2_expenditure.ID = 1 OR retail2_expenditure.ID = 2);
     select * from loyalist;
     SELECT retailer, count(household) as loyalist from loyalist
     group by retailer
     order by count(household) desc limit 2;
     
     -- iii. Where do they live? Plot the distribution by state. 
     # one retailer
	 SELECT hh_state, count(hh_id) from dta_at_hh,expenditure1
     WHERE dta_at_hh.hh_id=expenditure1.household
     group by hh_state;
     # two retailers
     SELECT hh_state, count(hh_id) from dta_at_hh,expenditure2
     WHERE dta_at_hh.hh_id=expenditure2.household
     group by hh_state;

-- Plot with the distribution:
	-- i Average number of items purchased on a given month.
     drop table if exists YM;
     create table YM    
     SELECT *,DATE_FORMAT(str_to_date(TC_date, '%Y-%m-%d'),'%Y-%m') as YM FROM dta_at_tc;

     SELECT * FROM ym;
	 SELECT * FROM dta_at_tc_upc;
     
     drop table if exists ym_upc;
     create table ym_upc
	 SELECT ym.ym,ym.hh_id,ym.tc_id,dta_at_tc_upc.quantity_at_TC_prod_id,dta_at_tc_upc.prod_id
     FROM ym,dta_at_tc_upc
     WHERE ym.tc_id=dta_at_tc_upc.tc_id;
     
     select ym, sum(quantity_at_TC_prod_id)/count(distinct hh_id) 
     as average_purchase_items 
     from ym_upc
     group by ym;

	-- ii Average number of shopping trips per month.
	SELECT ym, count(tc_id)/count(distinct hh_id) as average_shopping_trips FROM ym
    GROUP BY ym.ym;
    
    -- iii. Average number of days between 2 consecutive shopping trips.
    DROP TABLE IF EXISTS TC_day1;
     CREATE TABLE TC_day1
	   SELECT hh_id, str_to_date(TC_date, '%Y-%m-%d') as date1, ROW_NUMBER() OVER (ORDER BY hh_id, str_to_date(TC_date, '%Y-%m-%d')) AS ID  FROM dta_at_TC
       order by ID;
       
     DROP TABLE IF EXISTS TC_day2;
     CREATE TABLE TC_day2
	   SELECT *, 1 + ID AS ID_2 FROM TC_day1 
       order by ID_2;
	
     DROP TABLE IF EXISTS TC_day;
     CREATE TABLE TC_day
	 SELECT    A.date1       as first_date  , 
			   B.date1       as second_date , 
               A.hh_id       as household,
          datediff(A.date1  , B.date1) AS TIME_WINDOW_SIZE
	 FROM    
	 TC_day1 AS A
	 INNER  JOIN
	 TC_day2 AS B
	 ON     A.ID = B.ID_2 and A.hh_id = B.hh_id;
     
     select household,avg(TIME_WINDOW_SIZE) from TC_day
     GROUP BY household;
     
-- c. Answer and reason the following questions:
--
--
-- Private Labeled products are the products with the same brand as the supermarket. In the data set they appear labeled as ‘CTL BR’  
   -- i What are the product categories that have proven to be more “Private labelled”
     DROP TABLE IF EXISTS CTL;
     CREATE TABLE CTL  
     select department_at_prod_id,count(distinct prod_id) as CTL from dta_at_prod_id 
     where brand_at_prod_id = "CTL BR"
     GROUP BY department_at_prod_id;

     DROP TABLE IF EXISTS CTL2;
     CREATE TABLE CTL2  
     select department_at_prod_id,count(distinct prod_id) as CTL2 from dta_at_prod_id 
     GROUP BY department_at_prod_id;

	 drop table if exists ctl_final;
     create table ctl_final
     SELECT distinct CTL.department_at_prod_id, CTL.CTL, CTL2.CTL2 FROM CTL,CTL2
     where ctl.department_at_prod_id = ctl2.department_at_prod_id;
	 
     SELECT department_at_prod_id, sum(ctl)/sum(ctl2) AS private_label_percent
     from ctl_final
     group by department_at_prod_id;
    
   -- ii Is the expenditure share in Private Labeled products constant across months? 
     DROP TABLE IF EXISTS expenditure_share1;
     CREATE TABLE expenditure_share1  
     select ym.ym,sum(dta_at_tc_upc.total_price_paid_at_TC_prod_id) as sum_expenditure_ctl from ym,dta_at_prod_id,dta_at_tc_upc
     where ym.tc_id=dta_at_tc_upc.tc_id AND dta_at_prod_id.prod_id=dta_at_tc_upc.prod_id
     AND dta_at_prod_id.brand_at_prod_id = "CTL BR"
     GROUP BY ym.ym;

     DROP TABLE IF EXISTS expenditure_share2;
     CREATE TABLE expenditure_share2  
     select ym.ym,sum(dta_at_tc_upc.total_price_paid_at_TC_prod_id) as sum_expenditure_total from ym,dta_at_prod_id,dta_at_tc_upc
     where ym.tc_id=dta_at_tc_upc.tc_id AND dta_at_prod_id.prod_id=dta_at_tc_upc.prod_id
     GROUP BY ym.ym;
     
	 drop table if exists expenditure_share_final;
     create table expenditure_share_final
     SELECT distinct expenditure_share1.ym,expenditure_share1.sum_expenditure_ctl as exp1, expenditure_share2.sum_expenditure_total as exp2 FROM expenditure_share1, expenditure_share2
     where expenditure_share1.ym = expenditure_share2.ym;
	 select * from expenditure_share_final;
     
     SELECT ym,sum(exp1)/sum(exp2) AS private_label_percent
     from expenditure_share_final
     group by ym;
     -- iii. Cluster households in three income groups, Low, Medium and High. Report the average monthly expenditure on grocery. 
     -- Study the % of privadta_at_tc_upcte label share in their monthly expenditures. Use visuals to represent the intuition you are suggesting. 
     
     -- Report the  average monthly expenditure on grocery.
     DROP TABLE IF EXISTS income_group;
     CREATE TABLE income_group
		SELECT *,
		1*(hh_income<11)+2*(hh_income>=11 AND hh_income<19)+3*(hh_income>=19) as income_group
		FROM dta_at_hh;
	
     SELECT * FROM income_group;
     SELECT * FROM ym;

    drop table if exists monthly_expenditure;
    create table monthly_expenditure
	SELECT income_group.income_group,sum(ym.TC_total_spent)/count(distinct ym.ym) as group_avg FROM income_group,ym
	WHERE income_group.hh_id=ym.hh_id
	GROUP BY income_group.income_group;
    select * from monthly_expenditure;
     
	-- Study the % of private label share in their monthly expenditures. Use visuals to represent the intuition you are suggesting. 
    drop table fake_tc_upc;
    create table fake_tc_upc
    select tc_id, prod_id from dta_at_tc_upc;
    
    drop table dta_at_tc_upc;
    
    create table fake_prod_id
    select prod_id, brand_at_prod_id from dta_at_prod_id;
    
    drop table dta_at_prod_id;
    
    ### link 4 tables
	DROP TABLE IF EXISTS monthly_expenditure_ctl1;
	create temporary table monthly_expenditure_ctl1 
	SELECT income_group.income_group as income_group, ym.tc_id ,ym.tc_total_spent,ym.ym FROM income_group,  ym
	WHERE income_group.hh_id=ym.hh_id;
    
    select * from monthly_expenditure_ctl1;
    
    DROP TABLE IF EXISTS monthly_expenditure_ctl2;
	create temporary table monthly_expenditure_ctl2
    SELECT monthly_expenditure_ctl1.income_group,fake_tc_upc.prod_id,monthly_expenditure_ctl1.tc_total_spent,monthly_expenditure_ctl1.ym FROM monthly_expenditure_ctl1 ,fake_tc_upc
    WHERE monthly_expenditure_ctl1.tc_id=fake_tc_upc.tc_id;

	DROP TABLE IF EXISTS monthly_expenditure_ctl3;
    create temporary table monthly_expenditure_ctl3
    SELECT monthly_expenditure_ctl2.income_group, fake_prod_id.brand_at_prod_id,monthly_expenditure_ctl2.tc_total_spent,monthly_expenditure_ctl2.ym FROM monthly_expenditure_ctl2,fake_prod_id
    WHERE monthly_expenditure_ctl2.prod_id=fake_prod_id.prod_id;
    SELECT count(*) FROM monthly_expenditure_ctl3
    WHERE brand_at_prod_id = "CTL BR";

    # create CTL monthly avg spent
	DROP TABLE IF EXISTS monthly_expenditure_ctl_percentage;
    create temporary table monthly_expenditure_ctl_percentage
	select monthly_expenditure_ctl3.income_group,sum(monthly_expenditure_ctl3.tc_total_spent)/count(distinct monthly_expenditure_ctl3.ym) as group_avg
	from monthly_expenditure_ctl3
	WHERE brand_at_prod_id = "CTL BR"
    GROUP BY monthly_expenditure_ctl3.income_group;
    
    #create total montly avg spent
  	DROP TABLE IF EXISTS monthly_expenditure_percentage;
    create temporary table monthly_expenditure_percentage
	select monthly_expenditure_ctl3.income_group,sum(monthly_expenditure_ctl3.tc_total_spent)/count(distinct monthly_expenditure_ctl3.ym) as group_avg
	from monthly_expenditure_ctl3
    GROUP BY monthly_expenditure_ctl3.income_group;
  
    select * from monthly_expenditure_percentage;


	select monthly_expenditure_ctl_percentage.income_group,monthly_expenditure_ctl_percentage.group_avg/monthly_expenditure_percentage.group_avg AS percentage
	from monthly_expenditure_ctl_percentage,monthly_expenditure_percentage
	WHERE monthly_expenditure_ctl_percentage.income_group=monthly_expenditure_percentage.income_group;
        
	use db_consumer_panel;
	select quantity_at_TC_prod_id as number_items_purchased, 
    total_price_paid_at_TC_prod_id/quantity_at_TC_prod_id as item_average_price 
    from dta_at_TC_upc;
     
