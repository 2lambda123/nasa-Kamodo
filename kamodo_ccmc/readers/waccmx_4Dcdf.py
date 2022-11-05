# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 15:57:01 2022

@author: rringuet
files given have one hour of data, open at end (days since 1979-01-01 00:00:00)
lon and mlon need wrapping
lon is 0-360 (shape=144), mlon is -180 to 180 (shape=80)
lat (shape=96) and mlat (shape=97) include both poles
two pressure level variables:
    lev.shape = 130 at midpoints (hPa)
    ilev.shape = 131 at interfaces (hPa)
data structure order = (time, lev/ilev, lat/mlat, lon/mlon)
"""

# starts with variables from the h1 files. No h2 files in this set
model_varnames = {'co2vmr': ['mmr_CO2', 'co2 volume mixing ratio', 0,
                             'GDZ', 'sph', ['time'], ''],
                  'ch4vmr': ['mmr_CH4', 'ch4 volume mixing ratio', 0,
                             'GDZ', 'sph', ['time'], ''],
                  'n2ovmr': ['mmr_N2O', 'n2o volume mixing ratio', 0,
                             'GDZ', 'sph', ['time'], ''],
                  'f11vmr': ['mmr_F11', 'f11 volume mixing ratio', 0,
                             'GDZ', 'sph', ['time'], ''],
                  'f12vmr': ['mmr_F12', 'f12 volume mixing ratio', 0,
                             'GDZ', 'sph', ['time'], ''],
                  'sol_tsi': ['TSI', 'total solar irradiance', 0, 'GDZ', 'sph',
                              ['time'], 'W/m**2'],
                  'colat_crit1': ['Colat1', 'First co-latitude of electro-' +
                                  'potential critical angle', 0, 'GDZ', 'sph',
                                  ['time'],  'degrees'],
                  'colat_crit2': ['Colat2', 'Second co-latitude of electro-' +
                                  'potential critical angle', 0, 'GDZ', 'sph',
                                  ['time'], 'degrees'],
                  'ED1': ['E_east', 'ED1: Eastward Electric Field', 0,
                          'MAG', 'sph', ['time', 'mlon', 'mlat'], 'V/m'],
                  'ED2': ['E_equator', 'ED2: Equatorward Electric Field', 0,
                          'MAG', 'sph', ['time', 'mlon', 'mlat'], 'V/m'],
                  'EDYN_ZIGM11_PED': ['Sigma_P', 'Pedersen Conductance', 0,
                                      'MAG', 'sph', ['time', 'mlon', 'mlat'],
                                      'S'],
                  'EDYN_ZIGM2_HAL': ['Sigma_H', 'Hall Conductance', 0, 'MAG',
                                     'sph', ['time', 'mlon', 'mlat'], 'S'],
                  'ElecColDens': ['TEC', 'Electron Column Density', 0, 'GDZ',
                                  'sph', ['time', 'lon', 'lat'], '10**16/m**2'],
                  'H': ['Hyd_ilev', 'H concentration', 0, 'GDZ', 'sph',
                        ['time', 'lon', 'lat', 'ilev'], 'mol/mol'],
                  'H_2': ['Hyd', 'H concentration', 0, 'GDZ', 'sph',
                        ['time', 'lon', 'lat', 'height'], 'mol/mol'],
                  'O': ['Oxy_ilev', 'O concentration', 0, 'GDZ', 'sph',
                        ['time', 'lon', 'lat', 'ilev'], 'mol/mol'],
                  'O_2': ['Oxy', 'O concentration', 0, 'GDZ', 'sph',
                        ['time', 'lon', 'lat', 'height'], 'mol/mol'],
                  'O2': ['O2_ilev', 'O2 concentration', 0, 'GDZ', 'sph',
                         ['time', 'lon', 'lat', 'ilev'], 'mol/mol'],
                  'O2_2': ['O2', 'O2 concentration', 0, 'GDZ', 'sph',
                         ['time', 'lon', 'lat', 'height'], 'mol/mol'],
                  'OMEGA': ['v_up_ilev', 'Vertical velocity (pressure)', 0, 'GDZ',
                            'sph', ['time', 'lon', 'lat', 'ilev'], 'Pa/s'],
                  'OMEGA_2': ['v_up', 'Vertical velocity (pressure)', 0, 'GDZ',
                            'sph', ['time', 'lon', 'lat', 'height'], 'Pa/s'],
                  'PHIM2D': ['phi', 'PHIM2D: Electric Potential', 0, 'MAG',
                             'sph', ['time', 'mlon', 'mlat'], 'V'],
                  'PS': ['P_surface', 'Surface pressure', 0, 'GDZ', 'sph',
                         ['time', 'lon', 'lat'], 'Pa'],
                  'T': ['T_ilev', 'Temperature', 0, 'GDZ', 'sph',
                        ['time', 'lon', 'lat', 'ilev'], 'K'],
                  'T_2': ['T', 'Temperature', 0, 'GDZ', 'sph',
                        ['time', 'lon', 'lat', 'height'], 'K'],
                  'TElec': ['T_e_ilev', 'Electron Temperature', 0, 'GDZ', 'sph',
                            ['time', 'lon', 'lat', 'ilev'], 'K'],
                  'TElec_2': ['T_e', 'Electron Temperature', 0, 'GDZ', 'sph',
                            ['time', 'lon', 'lat', 'height'], 'K'],
                  'TIon': ['T_i_ilev', 'Ion Temperature', 0, 'GDZ', 'sph',
                           ['time', 'lon', 'lat', 'ilev'], 'K'],
                  'TIon_2': ['T_i', 'Ion Temperature', 0, 'GDZ', 'sph',
                           ['time', 'lon', 'lat', 'height'], 'K'],
                  'U': ['v_east_ilev', 'Zonal wind', 0, 'GDZ', 'sph',
                        ['time', 'lon', 'lat', 'ilev'], 'm/s'],
                  'U_2': ['v_east', 'Zonal wind', 0, 'GDZ', 'sph',
                        ['time', 'lon', 'lat', 'height'], 'm/s'],
                  'UI': ['vi_east_ilev', 'UI Zonal ion drift from edynamo', 0,
                         'GDZ', 'sph', ['time', 'lon', 'lat', 'ilev'], 'm/s'],
                  'UI_2': ['vi_east', 'UI Zonal ion drift from edynamo', 0,
                         'GDZ', 'sph', ['time', 'lon', 'lat', 'height'], 'm/s'],
                  'V': ['v_north_ilev', 'Meridional wind', 0, 'GDZ', 'sph',
                        ['time', 'lon', 'lat', 'ilev'], 'm/s'],
                  'V_2': ['v_north', 'Meridional wind', 0, 'GDZ', 'sph',
                        ['time', 'lon', 'lat', 'height'], 'm/s'],
                  'VI': ['vi_north_ilev', 'VI Meridional ion drift from edynamo',
                         0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'ilev'], 'm/s'],
                  'VI_2': ['vi_north', 'VI Meridional ion drift from edynamo',
                         0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'height'], 'm/s'],
                  'WI': ['vi_up_ilev', 'WI Vertical ion drift from edynamo',
                         0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'ilev'], 'm/s'],
                  'WI_2': ['vi_up', 'WI Vertical ion drift from edynamo',
                         0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'height'], 'm/s'],
                  'Z3': ['H_geopot_ilev', 'Geopotential Height (above sea level)',
                         0, '', 'sph', ['time', 'lon', 'lat', 'ilev'], 'm'],
                  'e': ['e_ilev', 'e concentration', 0, 'GDZ', 'sph',
                        ['time', 'lon', 'lat', 'ilev'], 'mol/mol'],
                  'e_2': ['e', 'e concentration', 0, 'GDZ', 'sph',
                        ['time', 'lon', 'lat', 'height'], 'mol/mol'],
                  'RHO_CLUBB': ['rho_ilev1', 'Air density', 0, 'GDZ', 'sph',
                                ['time', 'lon', 'lat', 'ilev1'], 'kg/m**3'],
                  'RHO_CLUBB_lev': ['rho_ilev', 'Air density', 0, 'GDZ', 'sph',
                                    ['time', 'lon', 'lat', 'ilev'], 'kg/m**3'],
                  'RHO_CLUBB_lev_2': ['rho', 'Air density', 0, 'GDZ', 'sph',
                                      ['time', 'lon', 'lat', 'height'],
                                       'kg/m**3'],

                  # variables in h1 files also in h3 files
                  'Z3GM': ['H_geomet_ilev', 'Geometric height', 0, 'GDZ', 'sph',
                           ['time', 'lon', 'lat', 'ilev'], 'm'],

                  # variables from the h2 files (also in h3 files!)
                  'EDens': ['N_e_ilev', 'e Number Density (sum of O2+,NO+,N2+,O+)', 0, 'GDZ', 'sph', 
                            ['time', 'lon', 'lat', 'ilev'], 'cm**3'],
                  'EDens_2': ['N_e', 'e Number Density (sum of O2+,NO+,N2+,O+)', 0, 'GDZ', 'sph', 
                            ['time', 'lon', 'lat', 'height'], 'cm**3'],
                  'HMF2': ['HmF2', 'Height of the F2 Layer', 0, 'GDZ', 'sph',
                           ['time', 'lat', 'lon'] , 'km'],
                  'NMF2': ['NmF2', 'Peak Density of the F2 Layer', 0, 'GDZ', 'sph',
                           ['time', 'lat', 'lon'] , '1/cm**3'],
                  'OPLUS': ['N_Oplus_ilev', 'O+ number density', 0, 'GDZ', 'sph',
                            ['time', 'lon', 'lat', 'ilev'], '1/cm**3'],
                  'OPLUS_2': ['N_Oplus', 'O+ number density', 0, 'GDZ', 'sph',
                            ['time', 'lon', 'lat', 'height'], '1/cm**3'],

                  # variables from the h3 files
                  'CO2': ['CO2_ilev', 'CO2 concentration', 0, 'GDZ', 'sph',
                          ['time', 'lon', 'lat', 'ilev'], 'mol/mol'],
                  'CO2_2': ['CO2', 'CO2 concentration', 0, 'GDZ', 'sph',
                          ['time', 'lon', 'lat', 'height'], 'mol/mol'],
                  # 'EKGW': ['EKGW_ilev1', 'Effective Kzz due to diffusion by gravity waves', 0, 'GDZ', 'sph', 
                  #           ['time', 'lon', 'lat', 'ilev1'], 'm**2/s'],
                  #'EKGW_2': ['EKGW', 'Effective Kzz due to diffusion by gravity waves', 0, 'GDZ', 'sph', 
                  #          ['time', 'lon', 'lat', 'height'], 'm**2/s'],
                  'N': ['Nit_ilev', 'N concentration', 0, 'GDZ', 'sph',
                        ['time', 'lon', 'lat', 'ilev'], 'mol/mol'],
                  'N_2': ['Nit', 'N concentration', 0, 'GDZ', 'sph',
                        ['time', 'lon', 'lat', 'height'], 'mol/mol'],
                  'NO': ['NO_ilev', 'NO concentration', 0, 'GDZ', 'sph',
                         ['time', 'lon', 'lat', 'ilev'], 'mol/mol'],
                  'NO_2': ['NO', 'NO concentration', 0, 'GDZ', 'sph',
                         ['time', 'lon', 'lat', 'height'], 'mol/mol'],
                  'OpDens': ['N_Oplus_ilev', 'O+ Number Density', 0, 'GDZ', 'sph',
                             ['time', 'lon', 'lat', 'ilev'], '1/cm**3'],
                  'OpDens_2': ['N_Oplus', 'O+ Number Density', 0, 'GDZ', 'sph',
                             ['time', 'lon', 'lat', 'height'], '1/cm**3'],
                  'QCO2': ['Q_CO2_ilev', 'CO2 cooling', 0, 'GDZ', 'sph',
                           ['time', 'lon', 'lat', 'ilev'], 'K/s'],
                  'QCO2_2': ['Q_CO2', 'CO2 cooling', 0, 'GDZ', 'sph',
                           ['time', 'lon', 'lat', 'height'], 'K/s'],
                  'QHC2S': ['Q_HC2S_ilev', 'Cooling to Space', 0, 'GDZ', 'sph',
                            ['time', 'lon', 'lat', 'ilev'], 'K/s'],
                  'QHC2S_2': ['Q_HC2S', 'Cooling to Space', 0, 'GDZ', 'sph',
                            ['time', 'lon', 'lat', 'height'], 'K/s'],
                  'QJOULE': ['Q_Joule_ilev', 'Joule Heat', 0, 'GDZ', 'sph',
                             ['time', 'lon', 'lat', 'ilev'], 'K/s'],
                  'QJOULE_2': ['Q_Joule', 'Joule Heat', 0, 'GDZ', 'sph',
                             ['time', 'lon', 'lat', 'height'], 'K/s'],
                  'QNO': ['Q_NO_ilev', 'NO cooling', 0, 'GDZ', 'sph',
                          ['time', 'lon', 'lat', 'ilev'], 'K/s'],
                  'QNO_2': ['Q_NO', 'NO cooling', 0, 'GDZ', 'sph',
                          ['time', 'lon', 'lat', 'height'], 'K/s'],
                  'QO3': ['Q_O3_ilev', 'O3 cooling', 0, 'GDZ', 'sph',
                          ['time', 'lon', 'lat', 'ilev'], 'K/s'],
                  'QO3_2': ['Q_O3', 'O3 cooling', 0, 'GDZ', 'sph',
                          ['time', 'lon', 'lat', 'height'], 'K/s'],
                  'QO3P': ['Q_O3P_ilev', 'O3P cooling', 0, 'GDZ', 'sph',
                           ['time', 'lon', 'lat', 'ilev'], 'K/s'],
                  'QO3P_2': ['Q_O3P', 'O3P cooling', 0, 'GDZ', 'sph',
                           ['time', 'lon', 'lat', 'height'], 'K/s'],
                  'QRS_TOT': ['Q_Total_ilev', 'Merged SW heating: QRS+QCP+QRS_EUV+QRS_CO2NIR+QRS_AUR+QTHERMAL',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'ilev'], 'K/s'],
                  'QRS_TOT_2': ['Q_Total', 'Merged SW heating: QRS+QCP+QRS_EUV+QRS_CO2NIR+QRS_AUR+QTHERMAL',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'height'], 'K/s'],
                  'SolIonRate_Tot': ['SolIonRate_Tot_ilev', 'reaction rate group', 0, 'GDZ', 'sph', 
                                      ['time', 'lon', 'lat', 'ilev'], '1/cm**3/s'],  # molecules/cm**3/s
                  'SolIonRate_Tot_2': ['SolIonRate_Tot', 'reaction rate group', 0, 'GDZ', 'sph', 
                                      ['time', 'lon', 'lat', 'height'], '1/cm**3/s'],  # molecules/cm**3/s
                  'TTGW': ['TTGW_ilev', 'T tendency - gravity wave drag', 0, 'GDZ', 'sph', 
                            ['time', 'lon', 'lat', 'ilev'], 'K/s'],
                  'TTGW_2': ['TTGW', 'T tendency - gravity wave drag', 0, 'GDZ', 'sph', 
                            ['time', 'lon', 'lat', 'height'], 'K/s'],
                  'UTGW_TOTAL': ['UTGW_TOTAL_ilev', 'Total U tendency due to gravity wave drag',
                                  0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'ilev'], 'm/s**2'],
                  'UTGW_TOTAL_2': ['UTGW_TOTAL', 'Total U tendency due to gravity wave drag',
                                  0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'height'], 'm/s**2'],

                  # variables from the h4 files
                  'OMEGA_08_COS': ['OMEGA_08_COS_ilev', 'vertical pressure velocity  8hr. cos coeff.',
                                   0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'ilev'], 'Pa/s'],
                  'OMEGA_08_COS_2': ['OMEGA_08_COS', 'vertical pressure velocity  8hr. cos coeff.',
                                   0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'height'], 'Pa/s'],
                  'OMEGA_08_SIN': ['OMEGA_08_SIN_ilev', 'vertical pressure velocity  8hr. sin coeff.',
                                   0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'ilev'], 'Pa/s'],
                  'OMEGA_08_SIN_2': ['OMEGA_08_SIN', 'vertical pressure velocity  8hr. sin coeff.',
                                   0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'height'], 'Pa/s'],
                  'OMEGA_12_COS': ['OMEGA_12_COS_ilev', 'vertical pressure velocity 12hr. cos coeff.',
                                   0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'ilev'], 'Pa/s'],
                  'OMEGA_12_COS_2': ['OMEGA_12_COS', 'vertical pressure velocity 12hr. cos coeff.',
                                   0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'height'], 'Pa/s'],
                  'OMEGA_12_SIN': ['OMEGA_12_SIN_ilev', 'vertical pressure velocity 12hr. sin coeff.',
                                   0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'ilev'], 'Pa/s'],
                  'OMEGA_12_SIN_2': ['OMEGA_12_SIN', 'vertical pressure velocity 12hr. sin coeff.',
                                   0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'height'], 'Pa/s'],
                  'OMEGA_24_COS': ['OMEGA_24_COS_ilev', 'vertical pressure velocity 24hr. cos coeff.',
                                   0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'ilev'], 'Pa/s'],
                  'OMEGA_24_COS_2': ['OMEGA_24_COS', 'vertical pressure velocity 24hr. cos coeff.',
                                   0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'height'], 'Pa/s'],
                  'OMEGA_24_SIN': ['OMEGA_24_SIN_ilev', 'vertical pressure velocity 24hr. sin coeff.',
                                   0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'ilev'], 'Pa/s'],
                  'OMEGA_24_SIN_2': ['OMEGA_24_SIN', 'vertical pressure velocity 24hr. sin coeff.',
                                   0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'height'], 'Pa/s'],
                  'T_08_COS': ['T_08_COS_ilev', 'Temperature  8hr. cos coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'ilev'], 'K'],
                  'T_08_COS_2': ['T_08_COS', 'Temperature  8hr. cos coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'height'], 'K'],
                  'T_08_SIN': ['T_08_SIN_ilev', 'Temperature  8hr. sin coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'ilev'], 'K'],
                  'T_08_SIN_2': ['T_08_SIN', 'Temperature  8hr. sin coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'height'], 'K'],
                  'T_12_COS': ['T_12_COS_ilev', 'Temperature 12hr. cos coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'ilev'], 'K'],
                  'T_12_COS_2': ['T_12_COS', 'Temperature 12hr. cos coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'height'], 'K'],
                  'T_12_SIN': ['T_12_SIN_ilev', 'Temperature 12hr. sin coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'ilev'], 'K'],
                  'T_12_SIN_2': ['T_12_SIN', 'Temperature 12hr. sin coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'height'], 'K'],
                  'T_24_COS': ['T_24_COS_ilev', 'Temperature 24hr. cos coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'ilev'], 'K'],
                  'T_24_COS_2': ['T_24_COS', 'Temperature 24hr. cos coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'height'], 'K'],
                  'T_24_SIN': ['T_24_SIN_ilev', 'Temperature 24hr. sin coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'ilev'], 'K'],
                  'T_24_SIN_2': ['T_24_SIN', 'Temperature 24hr. sin coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'height'], 'K'],
                  'U_08_COS': ['U_08_COS_ilev', 'Zonal wind  8hr. cos coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'ilev'], 'm/s'],
                  'U_08_COS_2': ['U_08_COS', 'Zonal wind  8hr. cos coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'height'], 'm/s'],
                  'U_08_SIN': ['U_08_SIN_ilev', 'Zonal wind  8hr. sin coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'ilev'], 'm/s'],
                  'U_08_SIN_2': ['U_08_SIN', 'Zonal wind  8hr. sin coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'height'], 'm/s'],
                  'U_12_COS': ['U_12_COS_ilev', 'Zonal wind 12hr. cos coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'ilev'], 'm/s'],
                  'U_12_COS_2': ['U_12_COS', 'Zonal wind 12hr. cos coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'height'], 'm/s'],
                  'U_12_SIN': ['U_12_SIN_ilev', 'Zonal wind 12hr. sin coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'ilev'], 'm/s'],
                  'U_12_SIN_2': ['U_12_SIN', 'Zonal wind 12hr. sin coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'height'], 'm/s'],
                  'U_24_COS': ['U_24_COS_ilev', 'Zonal wind 24hr. cos coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'ilev'], 'm/s'],
                  'U_24_COS_2': ['U_24_COS', 'Zonal wind 24hr. cos coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'height'], 'm/s'],
                  'U_24_SIN': ['U_24_SIN_ilev', 'Zonal wind 24hr. sin coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'ilev'], 'm/s'],
                  'U_24_SIN_2': ['U_24_SIN', 'Zonal wind 24hr. sin coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'height'], 'm/s'],
                  'V_08_COS': ['V_08_COS_ilev', 'Meridional wind  8hr. cos coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'ilev'], 'm/s'],
                  'V_08_COS_2': ['V_08_COS', 'Meridional wind  8hr. cos coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'height'], 'm/s'],
                  'V_08_SIN': ['V_08_SIN_ilev', 'Meridional wind  8hr. sin coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'ilev'], 'm/s'],
                  'V_08_SIN_2': ['V_08_SIN', 'Meridional wind  8hr. sin coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'height'], 'm/s'],
                  'V_12_COS': ['V_12_COS_ilev', 'Meridional wind 12hr. cos coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'ilev'], 'm/s'],
                  'V_12_COS_2': ['V_12_COS', 'Meridional wind 12hr. cos coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'height'], 'm/s'],
                  'V_12_SIN': ['V_12_SIN_ilev', 'Meridional wind 12hr. sin coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'ilev'], 'm/s'],
                  'V_12_SIN_2': ['V_12_SIN', 'Meridional wind 12hr. sin coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'height'], 'm/s'],
                  'V_24_COS': ['V_24_COS_ilev', 'Meridional wind 24hr. cos coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'ilev'], 'm/s'],
                  'V_24_COS_2': ['V_24_COS', 'Meridional wind 24hr. cos coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'height'], 'm/s'],
                  'V_24_SIN': ['V_24_SIN_ilev', 'Meridional wind 24hr. sin coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'ilev'], 'm/s'],
                  'V_24_SIN_2': ['V_24_SIN', 'Meridional wind 24hr. sin coeff.',
                               0, 'GDZ', 'sph', ['time', 'lon', 'lat', 'height'], 'm/s']
                  }

# lists of known variables per file type
# assume h1 file is always present
gvar_keys = {'h1v2': ['co2vmr', 'ch4vmr', 'n2ovmr', 'f11vmr', 'f12vmr',
                      'sol_tsi', 'colat_crit1', 'colat_crit2', 'ED1', 'ED2',
                      'EDYN_ZIGM11_PED', 'EDYN_ZIGM2_HAL', 'ElecColDens', 'H',
                      'O', 'O2', 'OMEGA', 'PHIM2D', 'PS', 'T', 'TElec', 'TIon',
                      'U', 'UI', 'V', 'VI', 'WI', 'Z3', 'e', 'RHO_CLUBB',
                      'RHO_CLUBB_lev', 'Z3GM'],
             # keys in h2 files that are not in the h1 files
             'h2v2': ['ED1', 'ED2', 'EDens', 'ElecColDens', 'HMF2', 'NMF2',
                      'OPLUS', 'TElec', 'TIon', 'UI', 'VI', 'WI', 'Z3'],
             # keys in h3 files that are not in the h1 files
             'h3v2': ['CO2', 'EDens', 'EKGW', 'N', 'NO', 'OpDens', 'QCO2',
                      'QHC2S', 'QJOULE', 'QNO', 'QO3', 'QO3P', 'QRS_TOT',
                      'SolIonRate_Tot', 'TTGW', 'UTGW_TOTAL', 'Z3GM'],
             # keys in the h4 files that are not in the h1 or h3 files
             'h4v2': ['OMEGA_08_COS', 'OMEGA_08_SIN', 'OMEGA_12_COS',
                      'OMEGA_12_SIN', 'OMEGA_24_COS', 'OMEGA_24_SIN',
                      'T_08_COS', 'T_08_SIN', 'T_12_COS', 'T_12_SIN',
                      'T_24_COS', 'T_24_SIN', 'U_08_COS', 'U_08_SIN',
                      'U_12_COS', 'U_12_SIN', 'U_24_COS', 'U_24_SIN',
                      'V_08_COS', 'V_08_SIN', 'V_12_COS', 'V_12_SIN',
                      'V_24_COS', 'V_24_SIN']}
# set up pressure level and height dependent equivalent variables
ilev_list = [value[0] for key, value in model_varnames.items()
             if value[5][-1] == 'ilev' if value not in
             ['H_geopot_ilev', 'H_geomet_ilev']]
ilev_replace = [item.split('_ilev')[0] for item in ilev_list if
                item not in ['H_geopot_ilev', 'H_geomet_ilev']]

'''
from glob import glob

file_dir = 'C:/Users/rringuet/Kamodo_Data/WACCMX/ftest.FXHIST.f19_f19_mg16.001/'
file_dir = 'D:/WACCMX/Jack_Wang_081222_IT_2/'
files = glob(file_dir+'*.nc')
dim_keys = ['mlat', 'mlon', 'lat', 'lon', 'time', 'ilev', 'ilev1']  # 'lev', 'ilev'
test = {key: [key, value.long_name, list(value.dimensions), value.units] for
        key,value in cdf_data.variables.items() if key not in dim_keys}
for key, value in cdf_data.variables.items():
    if key in dim_keys:
        continue
    if hasattr(cdf_data.variables[key], 'units'):
        print(key, value.longname, list(value.dimensions), value.units)
    else:
        print(key, value.longname, list(value.dimensions)
'''

from datetime import datetime, timezone, timedelta

def ts_to_hrs(time_val, filedate):
    '''Convert utc timestamp to hours since midnight on filedate.'''
    return (datetime.utcfromtimestamp(time_val).replace(tzinfo=timezone.utc) -
            filedate).total_seconds()/3600.


# times from file converted to seconds since midnight of filedate
# plotting input times will be datetime strings of format 'YYYY-MM-DD HH:mm:ss'
# filedate is self.filedate from iri object
# converts to hours since midnight of filedate for plotting
def MODEL():

    from kamodo import Kamodo
    from glob import glob
    from netCDF4 import Dataset
    from numpy import array, NaN, zeros, diff, median, squeeze
    from time import perf_counter
    import kamodo_ccmc.readers.reader_utilities as RU
    from waccmx_tocdf import convert_all


    class MODEL(Kamodo):
        '''WACCM-X model data reader.

        Inputs:
            file_dir: a string representing the file directory of the
                model output data.
                Note: This reader 'walks' the entire dataset in the directory.
            variables_requested = a list of variable name strings chosen from
                the model_varnames dictionary in this script, specifically the
                first item in the list associated with a given key.
                - If empty, the reader functionalizes all possible variables
                    (default)
                - If 'all', the reader returns the model_varnames dictionary
                    above for only the variables present in the given files.
                    Note: the fulltime keyword must be False to acheive this
                    behavior.
            filetime = boolean (default = False)
                - if False, the script fully executes.
                - If True, the script only executes far enough to determine the
                    time values associated with the chosen data.
                Note: The behavior of the script is determined jointly by the
                    filetime and fulltime keyword values.
            printfiles = boolean (default = False)
                - If False, the filenames associated with the data retrieved
                    ARE NOT printed.
                - If True, the filenames associated with the data retrieved ARE
                    printed.
            gridded_int = boolean (default = True)
                - If True, the variables chosen are functionalized in both the
                    standard method and a gridded method.
                - If False, the variables chosen are functionalized in only the
                    standard method.
            fulltime = boolean (default = True)
                - If True, linear interpolation in time between files is
                    included in the returned interpolator functions.
                - If False, no linear interpolation in time between files is
                    included.
            verbose = boolean (False)
                - If False, script execution and the underlying Kamodo
                    execution is quiet except for specified messages.
                - If True, be prepared for a plethora of messages.
        All inputs are described in further detail in
            KamodoOnboardingInstructions.pdf.

        Returns: a kamodo object (see Kamodo core documentation) containing all
            requested variables in functionalized form.
        '''
        def __init__(self, file_dir, variables_requested=[],
                     printfiles=False, filetime=False, gridded_int=True,
                     fulltime=True, verbose=False, **kwargs):
            super(MODEL, self).__init__(**kwargs)
            self.modelname = 'WACCM-X'
            t0 = perf_counter()

            # Check for converted files. If not present, convert all in dir
            self.conversion_test, file_dict = convert_all(file_dir)
            if not self.conversion_test:
                return
            file_list = []
            for key, files in file_dict.items():
                file_list.extend(files)
            self.filename = ''.join([f+',' for f in file_list])[:-1]

            # establish time attributes first, one value per file
            # different time grids in diff file patterns
            for key in file_dict.keys():
                date, datesec, time = [], [], []
                for file in file_dict[key]:
                    cdf_data = Dataset(file)
                    date.append(array(cdf_data.variables['time'])[0])
                    datesec.append(array(cdf_data.variables['datesec'])[0])
                    cdf_data.close()
                date = array(date)  # date is in days since 1979-01-01 00:00:00
                datesec = array(datesec)  # seconds since midnight on same day
                date -= int(date.min())  # reset to be from beginning of run
                for i in range(len(date)):
                    time.append(int(date[i])*24. + datesec[i]/3600.)  # hrs
                setattr(self, '_time_'+key, array(time))
            # datetime object for midnight on date
            self.filedate = datetime(1979, 1, 1, tzinfo=timezone.utc) +\
                timedelta(days=int(date[0]))
            # strings with timezone info chopped off (UTC anyway).
            # Format: ‘YYYY-MM-DD HH:MM:SS’
            self.datetimes = [
                (self.filedate+timedelta(hours=time[0])).isoformat(
                    sep=' ')[:19],
                (self.filedate+timedelta(hours=time[-1])).isoformat(
                    sep=' ')[:19]]
            self.filetimes = [datetime.timestamp(datetime.strptime(
                dt, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)) for dt
                in self.datetimes]   # utc timestamp
            if len(time) > 1:
                self.dt = diff(time).max()*3600.  # convert time res to sec
            else:
                self.dt = 3600.

            if filetime:  # boundary time added in file conversion process
                return  # return times as is to prevent recursion

            # if variables are given as integers, convert to standard names
            if len(variables_requested) > 0:
                if isinstance(variables_requested[0], int):
                    tmp_var = [value[0] for key, value in
                               model_varnames.items()
                               if value[2] in variables_requested]
                    variables_requested = tmp_var

            # perform initial check on variables_requested list
            if len(variables_requested) > 0 and fulltime and \
                    variables_requested != 'all':
                test_list = [value[0] for key, value in model_varnames.items()]
                err_list = [item for item in variables_requested if item not in
                            test_list]
                if len(err_list) > 0:
                    print('Variable name(s) not recognized:', err_list)

            # collect variable list per file
            self.gvar_dict, gvar_list, self.err_list = {}, [], []
            # dict[key] = [gvar_list, file] for each type of file
            self.total_ilev = [item for item in ilev_list if item
                               not in ['H_geopot_ilev', 'H_geomet_ilev']]
            self.total_replace = ilev_replace
            # dictionary mapping to navigate related variable names
            self.ilev_map = {item1: item2 for item1, item2 in
                             zip(self.total_replace, self.total_ilev)}
            if len(variables_requested) > 0 and variables_requested != 'all':
                # add variables from each files if the file exists and if
                # variables are requested from that file.
                for key in gvar_keys.keys():
                    self.gvar_dict[key] = self.somefile_variables(
                        key, gvar_keys[key], variables_requested,
                        file_dict)
                    gvar_list += self.gvar_dict[key][0]
                net_err = [value[0] for key, value in model_varnames.items()
                           if key not in gvar_list and value[0] in
                           self.err_list]
                if len(net_err) > 0:
                    print('Some requested variables are not available: ',
                          net_err)
            else:  # collect defaults
                # collect lists per file type
                for key in gvar_keys.keys():
                    self.gvar_dict[key] = self.allfile_variables(
                        key, gvar_keys[key], file_dict)
                    gvar_list += self.gvar_dict[key][0]

                # returns list of variables included in data files
                if not fulltime and variables_requested == 'all':
                    self.var_dict = {value[0]: value[1:] for key, value in
                                     model_varnames.items() if key in
                                     gvar_list}
                    # add non-ilev versions of the variables in the files
                    key_list = list(self.var_dict.keys())
                    for var_key in key_list:
                        if var_key in self.total_ilev:
                            # retrieve equivalent non-ilev variable name
                            new_key = [key for key, value in
                                       self.ilev_map.items() if value ==
                                       var_key][0]
                            # retrieve key for model_varnames mapping
                            model_key = [key for key, value in
                                         model_varnames.items() if
                                         value[0] == new_key][0]
                            # add to returned dictionary
                            self.var_dict[model_varnames[model_key][0]] =\
                                model_varnames[model_key][1:]
                    return

            # store data for each variable desired and all coordinate grids
            # need to leave files open for variable data
            variables, km = {}, None
            for key in file_dict.keys():
                # collect dimensions from first file
                time = getattr(self, '_time_'+key)  # time already calculated
                cdf_datah = Dataset(file_dict[key][0])
                for dim in cdf_datah.dimensions.keys():
                    if dim == 'ilev':
                        name = 'ilev1'
                    elif dim == 'lev':
                        name = 'ilev'
                    elif dim == 'time':
                        continue  # time already calculated, don't overwrite
                    else:
                        name = dim
                    setattr(self, '_'+name+'_'+key,
                            array(cdf_datah.variables[dim]))
                cdf_datah.close()  # close for dimensions data since now arrays
                
                # collect data from all files
                for t in range(len(time)):
                    cdf_datah = Dataset(file_dict[key][t])  # single time step
                    if 'Z3' in self.gvar_dict[key][0]:  # file variable names
                        if t == 0:  # get km_ilev grid (diff for each time)
                            km = [array(cdf_datah.variables['km_ilev'])]
                        else:
                            km.append(array(cdf_datah.variables['km_ilev']))
                    for var in self.gvar_dict[key][0]:
                        if t == 0:
                            variables[model_varnames[var][0]] =  {
                                'units': model_varnames[var][-1],
                                'data': [cdf_datah.variables[var]]}
                        else:
                            if var == 'Z3':
                                continue  # skip in favor of chunked version
                            variables[model_varnames[var][0]]['data'].append(
                                cdf_datah.variables[var])
            self._km_ilev = median(array(km), axis=0)  # median of time axis

            # collect chunked H_ilev function from h0v2 files
            h0_files = sorted(glob(file_dir+'*.h0v2.*.nc'))
            # does this stay open?
            variables['H_geopot_ilev']['data'] = [Dataset(f).variables['Z3']
                                                  for f in h0_files]
            self.start_idx = [0]
            for f in h0_files:  # determine starting indices of each time chunk
                c = Dataset(f)
                self.start_idx.append(self.start_idx[-1] +
                                      len(c.variables['time'].shape[0]))
                c.close()

            # store a few items
            self.missing_value = NaN
            self._registered = 0
            if verbose:
                print(f'Took {perf_counter()-t0:.6f}s to read in data')
            if printfiles:
                print(self.filename)
            print(f'Took {perf_counter()-t0:.6f}s to read in data')

            # register interpolators for each requested variable
            # rearrange to deal with H_ilev and H_ilev1 first if there
            varname_list = [key for key in variables.keys()]
            if 'H_geopot_ilev' in varname_list:
                varname_list.remove('H_geopot_ilev')
                varname_list = ['H_geopot_ilev'] + varname_list
            self.variables = {}
            t_reg = perf_counter()
            for varname in varname_list:
                self.variables[varname] = dict(
                    units=variables[varname]['units'],
                    data=variables[varname]['data'])
                # determine which time grid applies, preferring h1 files
                for key in self.gvar_dict.keys():
                    gvar = [key for key, value in model_varnames.items() if
                            value[0] == varname][0]
                    if gvar in self.gvar_dict[key][0]:
                        break
                # register the variables
                self.register_variable(varname, gridded_int, key) 
            if verbose:
                print(f'Took {perf_counter()-t_reg:.5f}s to register ' +
                      f'{len(varname_list)} variables.')
            if verbose:
                print(f'Took a total of {perf_counter()-t0:.5f}s to kamodofy' +
                      f' {len(varname_list)} variables.')

        # variable checks
        def variable_checks(self, variables_requested, g_varkeys_h,
                            cdf_datah_keys):
            '''Add pressure level variables if needed and perform variable
            checks for case where variables_requested is not empty.'''

            add_ilev = [var+'_ilev' for var in variables_requested if var
                        in self.total_replace]
            if len(add_ilev) > 0:
                add_ilev += ['H_geopot_ilev']
            new_var = variables_requested + add_ilev
            # remove replaced items and any items not expected to be in hx file
            short_var = [value[0] for key, value in model_varnames.items()
                         if value[0] in new_var and value[0] not in
                         self.total_replace and key in g_varkeys_h]
            gvar_listh = [key for key, value in model_varnames.items()
                          if value[0] in short_var and key
                          in cdf_datah_keys]

            # check for variables requested but not available
            if len(gvar_listh) != len(short_var):
                err_list = [value[0] for key, value in
                            model_varnames.items() if value[0] in
                            short_var and key not in cdf_datah_keys]
                for item in err_list:  # need a flat list
                    self.err_list.append(item)
                # add items to list, check full list later
            return gvar_listh

        # select desired variables from given file type
        def somefile_variables(self, h_type, g_varkeys_h, variables_requested,
                               file_dict):
            '''Add variables from desired file if file exists and if variables
            are requested.
            Inputs:
                - h_type is one of 'h2', 'h3', 'h4'.
                - g_varkeysh is a list of variables names known to exist in the
                    given file type.
                - variables_requested: a list of desired LaTeX variable names.
                - hx_files: a list of files for a given day.
            '''
            if h_type in file_dict.keys():
                cdf_datah = Dataset(file_dict[h_type][0])
                cdf_datah_keys = list(cdf_datah.variables.keys())
                cdf_datah.close()
                gvar_listh = self.variable_checks(variables_requested,
                                                  g_varkeys_h, cdf_datah_keys)
                return [gvar_listh, file_dict[h_type]]
            else:  # collect error list
                gvar_listh = self.variable_checks(variables_requested,
                                                  g_varkeys_h, [])
                return [gvar_listh, '']

        # return list of variables available in chosen file type
        def allfile_variables(self, h_type, g_varkeys_h, file_dict):
            '''Return list of variables from desired file if file exists.
            Inputs:
                - h_type is one of 'h2', 'h3', 'h4'.
                - g_varkeysh is a list of variables names known to exist in the
                    given file type.
            '''
            if h_type in file_dict.keys():
                cdf_datah = Dataset(file_dict[h_type][0])
                gvar_listh = [key for key, value in model_varnames.items()
                              if key in cdf_datah.variables.keys() and key in
                              g_varkeys_h]
                cdf_datah.close()
                return [gvar_listh, file_dict[h_type]]
            else:
                #print(h_type + ' file missing. The following variables ' +
                #      f'cannot be accessed: {g_varkeys_h}')
                return [[], '']

        # dimension agnostic registration
        def register_variable(self, varname, gridded_int, key):
            '''Registers and functionalizes the dataset. Converts to a 1D
            numpy array for time series data.'''
            
            # create the coordinate dictionary
            coord_list = [value[-2] for key, value in model_varnames.items()
                          if value[0] == varname][0]
            coord_str = [value[3]+value[4] for key, value in
                         model_varnames.items() if value[0] == varname][0]
            coord_dict = {'time': {'units': 'hr', 'data':
                                   getattr(self, '_time_'+key)}}
            if len(coord_list) == 1:  # convert 1D to array and functionalize
                tmp = []
                for cdf in self.variables[varname]['data']:
                    tmp.append(array(cdf)[0])  # single value per object
                self.variables[varname]['data'] = array(tmp)
                self = RU.Functionalize_Dataset(self, coord_dict, varname,
                                                self.variables[varname],
                                                gridded_int, coord_str,
                                                interp_flag=0)  # single array
                return
            for coord in coord_list[1:]:
                coord_dict[coord] = {'data': getattr(self,
                                                     '_'+coord+'_'+key)}
                if coord in ['lat', 'lon', 'mlon', 'mlat']:
                    coord_dict[coord]['units'] = 'deg'
                if coord in ['ilev', 'ilev1']:
                    coord_dict[coord]['units'] = 'hPa'

            if varname != 'H_geopot_ilev':
                # determine the operation to occur on each time slice
                def func(cdf_data_object):
                    tmp = array(cdf_data_object)
                    return squeeze(tmp)
    
                # functionalize the 3D or 4D dataset, series of time slices
                self = RU.Functionalize_Dataset(self, coord_dict, varname,
                                                self.variables[varname],
                                                gridded_int, coord_str,
                                                interp_flag=1, func=func)
            else:
                # function composition is too slow on top of a sliced interp
                # using chunked H_geopot_ilev instead
                self = RU.Functionalize_Dataset(self, coord_dict, varname,
                                                self.variables[varname],
                                                gridded_int, coord_str,
                                                interp_flag=2,
                                                start_idx=self.start_idx)
                
            if len(coord_list) < 4:  # remaining logic is for 4D data.
                return

            # create pressure level -> km function once per ilev type
            if varname == 'H_geopot_ilev' or varname in self.total_ilev:
                if varname == 'H_geopot_ilev' and hasattr(self, '_km_ilev'):
                    t_invert = perf_counter()  # create custom interp
                    print('Inverting H(ilev) function ...', end="")
                    new_varname = 'Plev'  # only one possible
                    # Import and call custom interpolator
                    from waccmx_ilevinterp import PLevelInterp
                    interpolator, interp_ijk = PLevelInterp(
                        self['H_geopot_ilev_ijk'], coord_dict['time']['data'],
                        coord_dict['lon']['data'], coord_dict['lat']['data'],
                        coord_dict['ilev']['data'])
                    units = 'hPa'
                    print(f'done in {perf_counter()-t_invert} s.')
                elif varname != 'H_geopot_ilev':  # define by function composition
                    new_varname = varname.split('_ilev')[0]
                    interpolator = varname+'(Plev)'
                    units = self.variables[varname]['units']

                # Register in kamodo object
                new_coord_units = {'time': 'hr', 'lon': 'deg',
                                   'lat': 'deg', 'height': 'km'}
                self.variables[new_varname] = {'units': units}
                self = RU.register_interpolator(self, new_varname,
                                                interpolator,
                                                new_coord_units)
                if varname in self.total_ilev:  # different if H vs not
                    interp_ijk = self[new_varname]

                # Create 'gridified' interpolators in the kamodo_object
                if gridded_int and hasattr(self, '_km_ilev'):
                    fake_data = zeros((2, 2, 2, 2))  # avoiding computation
                    coord_data = {key: value['data'] for key, value in
                                  coord_dict.items() if key in
                                  new_coord_units.keys()}  # exclude ilev
                    coord_data['height'] = self._km_ilev
                    self.variables[new_varname+'_ijk'] = {'data': fake_data,
                        'units': units}
                    gridded_interpolator = RU.define_griddedinterp(
                        self.variables[new_varname+'_ijk'], new_coord_units,
                        coord_data, interp_ijk)
                    self = RU.register_interpolator(
                        self, new_varname+'_ijk', gridded_interpolator,
                        new_coord_units)
            return
    return MODEL
