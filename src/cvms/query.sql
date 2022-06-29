select d.PER_NAME_MONTH
           ,cvms.monthly_snapshot_date_wid
           ,o.group_id
           ,o.branch_id
           ,c.edge_customer_number
           ,coalesce(c.company_name,c.customer_name) as customer_name
           ,c.master_customer_number
           ,c.master_company_name
           ,c.customer_since_dt
           ,c.customer_type_descr
           ,case when lt.lease_type_descr = 'Unknown' then null else lt.lease_type_descr end as lease_type_descr
           ,q.quote_number
           ,case when q.unit_number = 'Unknown' then null else q.unit_number end as unit_number
           ,q.lease_term
           ,q.liability_insurance_flg
           ,q.physical_damage_flg
           ,q.telematics_flg
           ,q.maintenance_management_flg
           ,q.custom_maintenance_flg
           ,q.full_maintenance_flg
           ,q.ame_flag
           ,q.fuel_card_id
           ,q.alternate_driver_flg
           ,case when q.alternate_driver_flg = 'Y' then 1 else 2 end as driver_type
           ,q.driver_contact_id
           ,initcap(q.driver_name) as driver_name
           ,q.driver_email
           ,q.driver_cell_phone
           ,CASE WHEN q.garage_street_address_1 = 'Unknown' THEN NULL ELSE q.garage_street_address_1 END garage_street_address_1
           ,CASE WHEN q.garage_street_address_2 = 'Unknown' THEN NULL ELSE q.garage_street_address_2 END garage_street_address_2
           ,CASE WHEN q.garage_street_address_3 = 'Unknown' THEN NULL ELSE q.garage_street_address_3 END garage_street_address_3
           ,CASE WHEN q.garage_street_address_4 = 'Unknown' THEN NULL ELSE q.garage_street_address_4 END garage_street_address_4
           ,CASE WHEN q.garage_city = 'N\/A' THEN NULL ELSE q.garage_city END garage_city
           ,CASE WHEN q.garage_county_name = 'N\/A' THEN NULL ELSE q.garage_county_name END garage_county_name
           ,CASE WHEN q.garage_state_prov = 'N\/A' THEN NULL ELSE q.garage_state_prov END garage_state_prov
           ,CASE WHEN q.garage_postal_code = 'N\/A' THEN NULL ELSE q.garage_postal_code END garage_postal_code
           ,case when q.garage_state_prov in ('AB', 'BC', 'MB', 'NB', 'NL', 'NS', 'NT', 'NU', 'ON', 'PE', 'QC', 'SK', 'YT') then 'CAN'
                 when q.garage_state_prov = 'N\/A' or q.garage_state_prov is null then NULL
                 else 'USA'
             end as garage_country
           ,q.maint_card_cost_code
           ,q.contract_mileage
           ,q.starting_mileage
           ,q.purchase_method
           ,q.vehicle_order_status
           ,case when q.lease_type = 'Net Lease' then NULL else q.depreciation_percentage*100 end as depreciation_percentage
           ,case q.pool_car_ind when '1' then 'Y' else 'N' end as pool_car_ind
           ,q.customer_vehicle_category
           ,aiq.lease_expiration_dt
           ,v.exterior_color
           ,v.interior_color
           ,v.user_entered_exp_annual_miles
           ,v.vehicle_id
           ,v.fleet_status
           ,case v.fleet_status
                when cast('NLA' as nvarchar2(5)) then cast('COVP' as nvarchar2(5))
                when cast('NL' as nvarchar2(5)) then cast('COV' as nvarchar2(5))
                else v.fleet_status
             end as reporting_fleet_status
           ,cast(
            case v.fleet_status
                when cast('L' as nvarchar2(50)) then cast('Leased Vehicle' as nvarchar2(50))
                when cast('NLA' as nvarchar2(50)) then cast('Client-Owned with Products' as nvarchar2(50))
                WHEN cast('NVP' as nvarchar2(50)) THEN cast('Non-Vehicles with Products' as nvarchar2(50))
                when cast('NL' as nvarchar2(50)) then cast('Client-Owned' as nvarchar2(50))
             end
             as nvarchar2(50)) as reporting_fleet_status_descr
           ,v.model_year
           ,v.make_descr
           ,v.model_descr
           ,v.series_descr
           ,v.veh_type_name
           ,case
                when q.customer_vehicle_id='Unknown' then NULL
                else q.customer_vehicle_id
             end as customer_vehicle_id
           ,v.vin
           ,v.license_plate_number
           ,v.license_plate_state
           ,case
                when to_char(v.license_plate_expiration_dt,'yyyy-mm-dd') = '1901-01-01' or v.license_plate_expiration_dt is null then null
                else v.license_plate_expiration_dt
             end as license_plate_expiration_dt
           ,v.gross_veh_weight
           ,v.gross_veh_weight_ratio_edit gvwr
           ,v.horsepower
           ,v.drive_train
           ,v.style_name
           ,v.num_of_cylinders
           ,v.cylinder_config
           ,v.transmission
           ,v.fuel_type
           ,vc.vehicle_class_descr
           ,qs.status_long_descr
           ,CASE WHEN qs.status_short_descr = cast('Unknown' as nvarchar2(50)) THEN cast('-' as nvarchar2(50)) ELSE cast(qs.status_short_descr as nvarchar2(50)) END status_short_descr
           ,case when qs.status_long_descr in ('Activated', 'Activated - Revised', 'Extended', 'Extended - Revised') then 'Y' else 'N' end as lease_active_flag
           ,ae.employee_display_name ae_employee_display_name
           ,ae.employee_eid ae_employee_eid
           ,ae.employee_email ae_employee_email
           ,am.employee_display_name am_employee_display_name
           ,am.employee_eid am_employee_eid
           ,am.employee_email am_employee_email
           ,case when cvms.eff_apprvd_quote_date_wid = -1 then NULL else to_date(to_char(cvms.eff_apprvd_quote_date_wid),'yyyymmdd') end eff_apprvd_quote_date
           ,case when cvms.eff_actvtn_quote_date_wid = -1 then NULL else to_date(to_char(cvms.eff_actvtn_quote_date_wid),'yyyymmdd') end eff_actvtn_quote_date
           ,case when cvms.delivery_quote_date_wid = -1 then NULL else to_date(to_char(cvms.delivery_quote_date_wid),'yyyymmdd') end delivery_quote_date
           ,cvms.months_in_service
           ,cvms.accumulated_prop_tax_amt
           ,CASE WHEN q.lease_type = 'Net Lease' THEN NULL ELSE cvms.current_rbv END current_rbv
           ,CASE WHEN q.lease_type = 'Net Lease' THEN NULL ELSE cvms.delivered_price END delivered_price
           ,cvms.fm_admin_fee
           ,cvms.fm_markup_down
           ,cvms.fm_service_sub_total fm_service_sub_total
           ,case when cvms.last_known_mileage = 0 or cvms.last_known_mileage is NULL then NULL
                 else cvms.last_known_mileage
             end as last_known_mileage
           ,case when to_char(cvms.last_known_mileage_date,'yyyy-mm-dd') = '1901-01-01' or cvms.last_known_mileage_date is NULL then NULL
                 else to_char(cvms.last_known_mileage_date,'yyyy-mm-dd')
             end as last_known_mileage_date
           ,cvms.lic_fee_amt
           ,cvms.lux_tax_amt
           ,CASE WHEN q.lease_type = 'Net Lease' THEN NULL ELSE cvms.mnthly_depreciation_amt END mnthly_depreciation_amt
           ,cvms.mnthly_int_adjstmnt_amt
           ,cvms.mnthly_interest_amt
           ,cvms.mnthly_management_fee
           ,cvms.mnthly_use_tax_amt
           ,cvms.service_charge
           ,cvms.total_mnthly_rent
           ,case when q.lease_type = 'Net Lease' then NULL
                 else coalesce(cvms.mnthly_management_fee,0)+coalesce(cvms.mnthly_interest_amt,0)+coalesce(cvms.mnthly_int_adjstmnt_amt,0)
             end as monthly_total_lease_charge
           ,coalesce(cvms.accumulated_prop_tax_amt,0)+coalesce(cvms.lux_tax_amt,0)+coalesce(cvms.lic_fee_amt,0) license_and_tax_amt
           ,coalesce(cvms.mnthly_fmx_amt,0) fm_monthly_amt
           ,cvms.license_admin_monthly_charge
           ,cvms.projected_current_mileage as projected_current_mileage
           ,cvms.odometer_diff_12mo
           ,cvms.odometer_diff_yago_12mo
           ,cvms.maint_amt_12mo
           ,cvms.cust_maint_amt_12mo
           ,cvms.ltd_maint_amt
           ,cvms.ltd_cust_maint_amt
           ,cvmsd.license_administration_flg
      from legacy.cust_veh_month_snp_f cvms
      join legacy.cust_veh_month_snp_d cvmsd on (cvms.monthly_snapshot_date_wid=cvmsd.monthly_snapshot_date_wid and cvms.vehicle_wid=cvmsd.vehicle_wid and cvms.quote_wid=cvmsd.quote_wid)
      join legacy.date_d d on (cvms.monthly_snapshot_date_wid=d.row_wid)
      join legacy.as_is_customer_dh_mv cdh on (cvms.customer_wid=cdh.customer_wid)
      join legacy.customer_d c on (cvms.customer_wid=c.customer_wid)
      join legacy.quote_d q on (cvms.quote_wid=q.quote_wid)
      join legacy.as_is_quote_d aiq on (cvms.quote_wid=aiq.quote_wid)
      join legacy.vehicle_d v on (cvms.vehicle_wid=v.vehicle_wid)
      join legacy.vehicle_class_d vc on (cvms.vehicle_class_wid=vc.vehicle_class_wid)
      join legacy.quote_status_d qs on (cvms.quote_status_wid=qs.quote_status_wid)
      join legacy.lease_type_d lt on (cvms.lease_type_wid=lt.lease_type_wid)
      join legacy.employee_d ae on (cvms.ae_employee_wid=ae.employee_wid)
      join legacy.employee_d am on (cvms.am_employee_wid=am.employee_wid)
      join legacy.org_d o on (cvms.org_wid=o.org_wid)
     where 1=1
       and ((v.fleet_status in ('L','NL','NLA','NVP') and qs.status_short_descr in ('Activated','Active-Rev','Extend-Rev','Extended','COV Active'))
              or
            (lt.lease_prod_number = 25 and qs.status_short_descr in ('Approved'))
           )
       and cvms.monthly_snapshot_date_wid = 20211231 --month snapshot date (last day of month)
       and cdh.ancestor_customer_number = 255105 --customer number to search
       and cdh.distance <= 99 --how far below the customer to search (i.e. just master = 1, master+subs <=99)
       --and q.unit_number = '23SCQV'
       --and o.group_branch = '1BL1'
