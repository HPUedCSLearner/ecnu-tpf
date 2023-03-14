
module ccsm_comp_mod

#define NEW_BUDGET
#define DEBUG

!#define MODULE_CPL 0
!#define MODULE_ATM 1
!#define MODULE_LND 2
!#define MODULE_ICE 3
!#define MODULE_OCN 4
!#define MODULE_GLC 5
!#define MODULE_WRF 6
!#define MODULE_GEA 7
!#define MODULE_CPLATM 8
!#define MODULE_CPLLND 9
!#define MODULE_CPLICE 10
!#define MODULE_CPLOCN 11
!#define MODULE_CPLGLC 12
!#define MODULE_CPLWRF 13
!#define MODULE_CPLGEA 14

!-------------------------------------------------------------------------------
!
! Purpose: Main program for NCAR CCSM4/cpl7. Can have different
!          land, sea-ice, and ocean models plugged in at compile-time.
!          These models can be either: stub, dead, data, or active
!          components or some combination of the above.
!
!               stub -------- Do nothing.
!               dead -------- Send analytic data back.
!               data -------- Send data back interpolated from input files.
!               prognostic -- Prognostically simulate the given component.
!
! Method: Call appropriate initialization, run (time-stepping), and 
!         finalization routines.
! 
!-------------------------------------------------------------------------------

   !----------------------------------------------------------------------------
   ! share code & libs
   !----------------------------------------------------------------------------

   use shr_kind_mod,      only: r8 => SHR_KIND_R8 
   use shr_kind_mod,      only: cs => SHR_KIND_CS
   use shr_kind_mod,      only: cl => SHR_KIND_CL
   use shr_sys_mod,       only: shr_sys_abort, shr_sys_flush
   use shr_const_mod,     only: shr_const_cday
   use shr_file_mod,      only: shr_file_setLogLevel, shr_file_setLogUnit
   use shr_file_mod,      only: shr_file_setIO, shr_file_getUnit
   use shr_scam_mod,      only: shr_scam_checkSurface
   use shr_map_mod,       only: shr_map_setDopole
   use shr_mpi_mod,       only: shr_mpi_min, shr_mpi_max
   use shr_mem_mod,       only: shr_mem_init, shr_mem_getusage
   use shr_cal_mod,       only: shr_cal_date2ymd
   use shr_orb_mod,       only: shr_orb_params
   use mct_mod            ! mct_ wrappers for mct lib
   use perf_mod
   use ESMF_Mod

   !----------------------------------------------------------------------------
   ! component model interfaces (init, run, final methods)
   !----------------------------------------------------------------------------
   use atm_comp_mct, only: atm_init_mct, atm_run_mct, atm_final_mct
!wangty modify
#ifdef wrf
   use wrf_comp_mct, only: wrf_init_mct, wrf_run_mct, wrf_final_mct  ! juanxiong he
   use geatm_comp_mct, only: geatm_init_mct, geatm_run_mct, geatm_final_mct  ! juanxiong he
#endif
   use lnd_comp_mct, only: lnd_init_mct, lnd_run_mct, lnd_final_mct
   use ocn_comp_mct, only: ocn_init_mct, ocn_run_mct, ocn_final_mct
   use ice_comp_mct, only: ice_init_mct, ice_run_mct, ice_final_mct
   use glc_comp_mct, only: glc_init_mct, glc_run_mct, glc_final_mct
#ifdef ESMF_INTERFACE
   use esmfshr_attribute_mod
   use atm_comp_mct, only: atm_register
   use lnd_comp_mct, only: lnd_register
   use ocn_comp_mct, only: ocn_register
   use ice_comp_mct, only: ice_register
   use glc_comp_mct, only: glc_register
#endif

   !----------------------------------------------------------------------------
   ! cpl7 modules
   !----------------------------------------------------------------------------

   !--- modules with public read/write data ---
   use seq_avdata_mod    ! drv aVects & associated domain, fraction, cdata
   use seq_diag_mct      ! diagnostic routines

   !--- other ---
   use seq_flds_indices  ! drv aVect field indicies, routines
   use seq_comm_mct      ! mpi comm data & routines, plus logunit and loglevel
   use seq_timemgr_mod   ! clock & alarm routines 
   use seq_infodata_mod  ! "infodata" gathers various control flags into one datatype
   use seq_cdata_mod     ! "cdata" type & methods (domain + decomp + infodata in one datatype)
   use seq_domain_mct    ! domain related routines
   use seq_flux_mct      ! flux calc routines
   use seq_frac_mct      ! domain fraction routines
   use seq_rest_mod      ! restart file routines
   use seq_hist_mod      ! history file routines
   use seq_io_mod        ! i/o subroutins

   !--- merging routines ---
!wangty modify
#ifdef wrf
   use mrg_x2w_mct      ! wrf merge gridded component (merging, history) by juanxiong he
   use mrg_x2c_mct      ! cam merge gridded component (merging, history) by juanxiong he
   use mrg_x2ca_mct      ! cam merge gridded component (merging, history) by juanxiong he
   use mrg_x2ge_mct      ! wrf merge gridded component (merging, history) by juanxiong he
#endif
   use mrg_x2a_mct      ! atm merge gridded component (merging, history)
   use mrg_x2l_mct      ! lnd merge gridded component
   use mrg_x2o_mct      ! ocn merge gridded component
   use mrg_x2i_mct      ! ice merge gridded component
   use mrg_x2g_mct      ! glc merge gridded component
   use mrg_x2s_mct      ! sno merge gridded component

   !--- mapping routines ---
!wangty modify
#ifdef wrf
   use map_camcam_mct   ! juanxiong he
   use map_wrfwrf_mct   ! juanxiong he
   use map_wrfcam_mct   ! juanxiong he
   use map_gcamcam_mct   ! juanxiong he
   use map_geagea_mct   ! juanxiong he
   use map_geacam_mct   ! juanxiong he
#endif
   use map_atmlnd_mct   ! atm to lnd coupler component
   use map_atmice_mct   ! atm to ice coupler component
   use map_atmocn_mct   ! atm to ocn coupler component
   use map_iceocn_mct   ! ice to ocn coupler component
   use map_rofocn_mct   ! roff to ocn coupler component
   use map_snoglc_mct   ! lnd/sno to glc coupler component
   use map_ocnocn_mct   ! ocn to ocn coupler component
   use map_iceice_mct   ! ice to ice coupler component
   use map_lndlnd_mct   ! lnd to lnd coupler component
   use map_rofrof_mct   ! lnd to lnd coupler component
   use map_atmatm_mct   ! atm to atm coupler component
   use map_glcglc_mct   ! glc to glc coupler component
   use map_snosno_mct   ! lnd/sno to lnd/sno coupler component

   implicit none

   private

   public ccsm_pre_init, ccsm_init, ccsm_run, ccsm_final
#ifdef ESMF_INTERFACE
   public ccsm_comp_register
#endif
   public timing_dir, mpicom_GLOID

#include <mpif.h>

   !----------------------------------------------------------------------------
   ! domains & related
   !----------------------------------------------------------------------------

   !--- domain decomps (MCT Global Seg Maps) ---
   type(mct_gsMap)  :: gsMap_aa    ! on component pes
   type(mct_gsMap)  :: gsMap_ll
   type(mct_gsMap)  :: gsMap_oo
   type(mct_gsMap)  :: gsMap_ii
   type(mct_gsMap)  :: gsMap_rr
   type(mct_gsMap)  :: gsMap_gg
   type(mct_gsMap)  :: gsMap_ss
!wangty modify
#ifdef wrf
   type(mct_gsMap)  :: gsMap_ww   !juanxiong he
   type(mct_gsMap)  :: gsMap_cc   !juanxiong he
   type(mct_gsMap)  :: gsMap_mm   !juanxiong he
   type(mct_gsMap)  :: gsMap_gege   !juanxiong he
   type(mct_gsMap)  :: gsMap_caca   !juanxiong he
#endif
   type(mct_gsMap)  :: gsMap_ax    ! on cpl pes
   type(mct_gsMap)  :: gsMap_lx
   type(mct_gsMap)  :: gsMap_ox
   type(mct_gsMap)  :: gsMap_ix
   type(mct_gsMap)  :: gsMap_rx
   type(mct_gsMap)  :: gsMap_gx
   type(mct_gsMap)  :: gsMap_sx
!wangty modify
#ifdef wrf
   type(mct_gsMap)  :: gsMap_cx  !juanxiong he
   type(mct_gsMap)  :: gsMap_wx  !juanxiong he
   type(mct_gsMap)  :: gsMap_mx   !juanxiong he
   type(mct_gsMap)  :: gsMap_cax  !juanxiong he
   type(mct_gsMap)  :: gsMap_gex  !juanxiong he
#endif
   !--- domain area correction factors (only defined on cpl pes) ---
   real(r8),pointer :: drv2mdl_aa(:), mdl2drv_aa(:)
   real(r8),pointer :: drv2mdl_ll(:), mdl2drv_ll(:)
   real(r8),pointer :: drv2mdl_ii(:), mdl2drv_ii(:)
   real(r8),pointer :: drv2mdl_oo(:), mdl2drv_oo(:)
   real(r8),pointer :: drv2mdl_rr(:), mdl2drv_rr(:)
   real(r8),pointer :: drv2mdl_gg(:), mdl2drv_gg(:)
   real(r8),pointer :: drv2mdl_ss(:), mdl2drv_ss(:)
!wangty modify
#ifdef wrf
   real(r8),pointer :: drv2mdl_ww(:), mdl2drv_ww(:)   ! juanxiong he
   real(r8),pointer :: drv2mdl_ge(:), mdl2drv_ge(:)   ! juanxiong he
#endif

   !--- domain equivalent 2d grid size ---
   integer          :: atm_nx, atm_ny  ! nx, ny of 2d grid, if known
   integer          :: lnd_nx, lnd_ny
   integer          :: ice_nx, ice_ny
   integer          :: ocn_nx, ocn_ny
   integer          :: rof_nx, rof_ny
   integer          :: glc_nx, glc_ny
   integer          :: sno_nx, sno_ny
   
   integer          :: MODULE_CPL=0!0
   integer          :: MODULE_ATM=1
   integer          :: MODULE_LND=2
   integer          :: MODULE_ICE=3
   integer          :: MODULE_OCN=4
   integer          :: MODULE_GLC=5
   integer          :: MODULE_WRF=6
   integer          :: MODULE_GEA=7
   integer          :: MODULE_CPLATM=8!8
   integer          :: MODULE_CPLLND=9!9
   integer          :: MODULE_CPLICE=10!10
   integer          :: MODULE_CPLOCN=11!11
   integer          :: MODULE_CPLGLC=12!12
   integer          :: MODULE_CPLWRF=13!13
   integer          :: MODULE_CPLGEA=14!14
   
   
!wangty modify
#ifdef wrf
   integer          :: wrf_nx, wrf_ny  ! juanxiong he
   integer          :: geatm_nx, geatm_ny  ! juanxiong he
#endif
   !----------------------------------------------------------------------------
   ! time management
   !----------------------------------------------------------------------------

   type (seq_timemgr_type), SAVE :: seq_SyncClock ! array of all clocks & alarm
   type (ESMF_Clock), SAVE       :: EClock_d      ! driver clock
   type (ESMF_Clock), SAVE       :: EClock_a
   type (ESMF_Clock), SAVE       :: EClock_l
   type (ESMF_Clock), SAVE       :: EClock_o
   type (ESMF_Clock), SAVE       :: EClock_i
   type (ESMF_Clock), SAVE       :: EClock_g
!wangty modify
#ifdef wrf
   type (ESMF_Clock)       :: EClock_w  ! juanxiong he for wrf/ccsm4 coupling
   type (ESMF_Clock)       :: EClock_ge  ! juanxiong he for wrf/ccsm4 coupling
#endif
   logical  :: restart_alarm          ! restart alarm
   logical  :: history_alarm          ! history alarm
   logical  :: histavg_alarm          ! history alarm
   logical  :: stop_alarm             ! stop alarm
   logical  :: atmrun_alarm           ! atm run alarm
!wangty modify
#ifdef wrf
   logical  :: wrfrun_alarm           ! wrf run alarm, juanxiong he
   logical  :: gearun_alarm           ! gea run alarm, juanxiong he
#endif
   logical  :: lndrun_alarm           ! lnd run alarm
   logical  :: icerun_alarm           ! ice run alarm
   logical  :: ocnrun_alarm           ! ocn run alarm
   logical  :: ocnnext_alarm          ! ocn run alarm on next timestep
   logical  :: glcrun_alarm           ! glc run alarm
   logical  :: tprof_alarm            ! timing profile alarm
   logical  :: t1hr_alarm             ! alarm every hour
   logical  :: t2hr_alarm             ! alarm every two hours 
   logical  :: t3hr_alarm             ! alarm every three hours 
   logical  :: t6hr_alarm             ! alarm every six hours 
   logical  :: t12hr_alarm            ! alarm every twelve hours 
   logical  :: t24hr_alarm            ! alarm every twentyfour hours 

   real(r8) :: days_per_year = 365.0  ! days per year

   integer  :: dtime                  ! dt of one coupling interval
   integer  :: ncpl                   ! number of coupling intervals per day
   integer  :: ymd                    ! Current date (YYYYMMDD)
   integer  :: year                   ! Current date (YYYY)
   integer  :: month                  ! Current date (MM)
   integer  :: day                    ! Current date (DD)
   integer  :: tod                    ! Current time of day (seconds)
   character(CL) :: orb_mode          ! orbital mode
   integer  :: orb_iyear              ! orbital year
   integer  :: orb_iyear_align        ! associated with model year
   integer  :: orb_cyear              ! orbital year for current orbital computation
   integer  :: orb_nyear              ! orbital year associated with currrent model year
   real(r8) :: orb_eccen              ! orbital eccentricity
   real(r8) :: orb_obliq              ! obliquity in degrees
   real(r8) :: orb_mvelp              ! moving vernal equinox long
   real(r8) :: orb_obliqr             ! Earths obliquity in rad
   real(r8) :: orb_lambm0             ! Mean long of perihelion at vernal equinox (radians)
   real(r8) :: orb_mvelpp             ! moving vernal equinox long

   !--- for documenting speed of the model ---
   character( 8) :: dstr              ! date string
   character(10) :: tstr              ! time string
   integer       :: begStep, endStep  ! Begining and ending step number
   real(r8)      :: simDays           ! Number of simulated days
   real(r8)      :: SYPD              ! Simulated years per day
   real(r8)      :: Time_begin        ! Start time
   real(r8)      :: Time_end          ! Ending time
   real(r8)      :: Time_bstep        ! Start time
   real(r8)      :: Time_estep        ! Ending time
   real(r8)      :: dtstep            ! delta time
   real(r8)      :: dtstep_acc        ! dtstep accumulator
   integer       :: dtstep_cnt        ! dtstep counter
   character(CL) :: timing_file       ! Local path to tprof filename
   character(CL) :: timing_dir        ! timing directory
   character(CL) :: tchkpt_dir        ! timing checkpoint directory

   !----------------------------------------------------------------------------
   ! control flags
   !----------------------------------------------------------------------------

   logical  :: atm_present            ! .true.  => atm is present
   logical  :: lnd_present            ! .true.  => land is present
   logical  :: ice_present            ! .true.  => ice is present
   logical  :: ocn_present            ! .true.  => ocn is present
   logical  :: rof_present            ! .true.  => land runoff is present
   logical  :: glc_present            ! .true.  => glc is present
!wangty modify
#ifdef wrf
   logical  :: wrf_present            ! .true.  => wrf is present, juanxiong he
   logical  :: geatm_present            ! .true.  => gea is present, juanxiong he
#endif
   logical  :: sno_present            ! .true.  => land sno is present

   logical  :: atm_prognostic         ! .true.  => atm comp expects input
   logical  :: lnd_prognostic         ! .true.  => lnd comp expects input
   logical  :: ice_prognostic         ! .true.  => ice comp expects input
   logical  :: ocn_prognostic         ! .true.  => ocn comp expects input
   logical  :: ocnrof_prognostic      ! .true.  => ocn comp expects runoff input
   logical  :: glc_prognostic         ! .true.  => glc comp expects input
!wangty modify
#ifdef wrf
   logical  :: wrf_prognostic         ! .true.  => wrf comp expects input, juanxiong he
   logical  :: geatm_prognostic         ! .true.  => gea comp expects input, juanxiong he
#endif
   logical  :: sno_prognostic         ! .true.  => sno comp expects input

   logical  :: dead_comps             ! .true.  => dead components 

   logical  :: single_column          ! scm mode logical
   real(r8) :: scmlon                 ! single column lon
   real(r8) :: scmlat                 ! single column lat
   logical  :: aqua_planet            ! aqua planet mode
   real(r8) :: nextsw_cday            ! radiation control
   logical  :: atm_aero               ! atm provides aerosol data
   real(r8) :: flux_epbalfact         ! precip factor

   logical  :: ocean_tight_coupling   ! couple ocn as frequently as lnd & ice
   logical  :: skip_ocean_run         ! skip the ocean model first pass
   logical  :: cpl2ocn_first          ! use to call initial cpl2ocn timer
   character(CS) :: aoflux_grid       ! grid for a/o flux calc: atm xor ocn 
   logical  :: run_barriers           ! barrier the component run calls

   logical       :: read_restart      ! local read restart flag
   character(CL) :: rest_file         ! restart file path + filename

   logical  :: domain_check           ! .true.  => check consistency of domains
   logical  :: shr_map_dopole         ! logical for dopole in shr_map_mod

   !--- history & budgets ---
   logical       :: do_budgets        ! heat/water budgets on
   logical       :: do_histinit       ! initial hist file
   logical       :: do_histavg        ! histavg on or off
   logical       :: do_hist_r2x       ! create aux files: r2x
   logical       :: do_hist_l2x       ! create aux files: l2x
   logical       :: do_hist_a2x24hr   ! create aux files: a2x
   logical       :: do_hist_a2x       ! create aux files: a2x
   logical       :: do_hist_a2x3hrp   ! create aux files: a2x 3hr precip
   logical       :: do_hist_a2x3hr    ! create aux files: a2x 3hr states
!  character(CL) :: hist_r2x_flds     = 'all'
!  character(CL) :: hist_l2x_flds     = 'all'
   character(CL) :: hist_a2x_flds     = 'Faxa_swndr:Faxa_swvdr:Faxa_swndf:Faxa_swvdf'
!  character(CL) :: hist_a2x24hr_flds = 'all'
   character(CL) :: hist_a2x3hrp_flds = 'Faxa_rainc:Faxa_rainl:Faxa_snowc:Faxa_snowl'
   character(CL) :: hist_a2x3hr_flds  = 'Sa_z:Sa_u:Sa_v:Sa_tbot:Sa_ptem:Sa_shum:Sa_dens:Sa_pbot:Sa_pslv:Faxa_lwdn'
   integer  :: budget_inst            ! instantaneous budget flag
   integer  :: budget_daily           ! daily budget flag
   integer  :: budget_month           ! monthly budget flag
   integer  :: budget_ann             ! annual budget flag
   integer  :: budget_ltann           ! long term budget flag for end of year writing
   integer  :: budget_ltend           ! long term budget flag for end of run writing

   ! --- other ---
   integer  :: k1,k2,k3               ! aVect field indices
   integer  :: ocnrun_count           ! number of times ocn run alarm went on
   logical  :: exists                 ! true if file exists
   integer  :: ierr                   ! MPI error return
   integer  :: rc                     ! return code
   logical  :: cdf64                  ! true => use 64 bit addressing in netCDF files

   character(*), parameter :: NLFileName = "drv_in"  ! input namelist filename

   integer  :: info_debug = 0         ! local info_debug level

   !----------------------------------------------------------------------------
   ! memory monitoring
   !----------------------------------------------------------------------------
   real(r8) :: msize,msize0,msize1     ! memory size (high water)
   real(r8) :: mrss ,mrss0 ,mrss1      ! resident size (current memory use)

   !----------------------------------------------------------------------------
   ! threading control
   !----------------------------------------------------------------------------
   integer  :: nthreads_GLOID         ! OMP global number of threads
   integer  :: nthreads_CPLID         ! OMP cpl number of threads
   integer  :: nthreads_ATMID         ! OMP atm number of threads
   integer  :: nthreads_LNDID         ! OMP lnd number of threads
   integer  :: nthreads_ICEID         ! OMP ice number of threads
   integer  :: nthreads_OCNID         ! OMP ocn number of threads
   integer  :: nthreads_GLCID         ! OMP glc number of threads
!wangty modify
#ifdef wrf 
   integer  :: nthreads_WRFID         ! OMP wrf number of threads, juanxiong he
   integer  :: nthreads_GEAID         ! OMP wrf number of threads, juanxiong he
#endif
   integer  :: pethreads_GLOID        ! OMP number of threads per task

   integer  :: nthreads_CPLATMID      ! OMP cpl-atm number of threads
   integer  :: nthreads_CPLLNDID      ! OMP cpl-lnd number of threads
   integer  :: nthreads_CPLICEID      ! OMP cpl-ice number of threads
   integer  :: nthreads_CPLOCNID      ! OMP cpl-ocn number of threads
   integer  :: nthreads_CPLGLCID      ! OMP cpl-glc number of threads
!wangty modify
#ifdef wrf
   integer  :: nthreads_CPLWRFID      ! OMP cpl-glc number of threads, juanxiong he
   integer  :: nthreads_CPLGEAID      ! OMP cpl-glc number of threads, juanxiong he
#endif
   logical  :: drv_threading          ! driver threading control

   !----------------------------------------------------------------------------
   ! communicator groups and related
   !----------------------------------------------------------------------------
   integer  :: Global_Comm
   integer  :: mpicom_GLOID           ! MPI global communicator
   integer  :: mpicom_CPLID           ! MPI cpl communicator
   integer  :: mpicom_ATMID           ! MPI atm communicator
   integer  :: mpicom_LNDID           ! MPI lnd communicator
   integer  :: mpicom_ICEID           ! MPI ice communicator
   integer  :: mpicom_OCNID           ! MPI ocn communicator
   integer  :: mpicom_GLCID           ! MPI glc communicator
!wangty modify
#ifdef wrf
   integer  :: mpicom_WRFID           ! MPI wrf communicator, juanxiong he
   integer  :: mpicom_GEAID           ! MPI wrf communicator, juanxiong he
#endif
   integer  :: mpicom_CPLATMID        ! MPI cpl-atm communicator
   integer  :: mpicom_CPLLNDID        ! MPI cpl-lnd communicator
   integer  :: mpicom_CPLICEID        ! MPI cpl-ice communicator
   integer  :: mpicom_CPLOCNID        ! MPI cpl-ocn communicator
   integer  :: mpicom_CPLGLCID        ! MPI cpl-glc communicator
!wangty modify
#ifdef wrf
   integer  :: mpicom_CPLWRFID        ! MPI cpl-wrf communicator, juanxiong he
   integer  :: mpicom_CPLGEAID        ! MPI cpl-wrf communicator, juanxiong he
#endif
   logical  :: iamroot_GLOID          ! GLOID masterproc
   logical  :: iamroot_CPLID          ! CPLID masterproc
   logical  :: iamroot_ATMID          ! ATMID masterproc
   logical  :: iamroot_LNDID          ! LNDID masterproc
   logical  :: iamroot_ICEID          ! ICEID masterproc
   logical  :: iamroot_OCNID          ! OCNID masterproc
   logical  :: iamroot_GLCID          ! GLCID masterproc
!wangty modify
#ifdef wrf
   logical  :: iamroot_WRFID          ! WRFID masterproc, juanxiong he
   logical  :: iamroot_GEAID          ! GEAID masterproc, juanxiong he
#endif
   logical  :: iamin_CPLID            ! pe associated with CPLID
   logical  :: iamin_ATMID            ! pe associated with ATMID
   logical  :: iamin_LNDID            ! pe associated with LNDID
   logical  :: iamin_ICEID            ! pe associated with ICEID
   logical  :: iamin_OCNID            ! pe associated with OCNID
   logical  :: iamin_GLCID            ! pe associated with GLCID
!wangty modify
#ifdef wrf
   logical  :: iamin_WRFID            ! pe associated with WRFID, juanxiong he
   logical  :: iamin_GEAID            ! pe associated with WRFID, juanxiong he
#endif
   logical  :: iamin_CPLATMID         ! pe associated with CPLATMID
   logical  :: iamin_CPLLNDID         ! pe associated with CPLLNDID
   logical  :: iamin_CPLICEID         ! pe associated with CPLICEID
   logical  :: iamin_CPLOCNID         ! pe associated with CPLOCNID
   logical  :: iamin_CPLGLCID         ! pe associated with CPLGLCID
!wangty modify
#ifdef wrf
   logical  :: iamin_CPLWRFID         ! pe associated with CPLWRFID, juanxiong he
   logical  :: iamin_CPLGEAID         ! pe associated with CPLWRFID, juanxiong he
#endif
   character(CL) :: complist          ! list of comps on this pe
   integer  :: iam_GLOID              ! pe number in global id
!wangty modify
#ifdef wrf
   integer, pointer :: atm_petlist(:), lnd_petlist(:), ice_petlist(:), ocn_petlist(:), glc_petlist(:), &
                       wrf_petlist(:), gea_petlist(:) ! juanxiong he
#else
   integer, pointer :: atm_petlist(:), lnd_petlist(:), ice_petlist(:), ocn_petlist(:), glc_petlist(:)
#endif
   !----------------------------------------------------------------------------
   ! formats
   !----------------------------------------------------------------------------
   character(*), parameter :: subname = '(seq_mct_drv)'
   character(*), parameter :: F00 = "('"//subname//" : ', 4A )"
   character(*), parameter :: F0L = "('"//subname//" : ', A, L6 )"
   character(*), parameter :: F0I = "('"//subname//" : ', A, 2i8 )"
   character(*), parameter :: F0R = "('"//subname//" : ', A, 2g23.15 )"
   character(*), parameter :: FormatA = '(A,": =============== ", A41,          " ===============")'
   character(*), parameter :: FormatD = '(A,": =============== ", A20,2I8,5x,   " ===============")'
   character(*), parameter :: FormatR = '(A,": =============== ", A31,F9.3,1x,  " ===============")'
   character(*), parameter :: FormatQ = '(A,": =============== ", A20,2F10.2,1x," ===============")'
!wangty modify
#ifdef wrf
   logical :: twoway_coupling ! juanxiong he
   integer :: twoway_nudging ! juanxiong he
   integer :: integration_phase ! juanxiong he
#endif
!===============================================================================
contains
!===============================================================================

!-------------------------------------------------------------------------------
!
!-------------------------------------------------------------------------------

subroutine ccsm_pre_init()

   !--------------------------------------------------------------------------
   ! Initialize MCT and MPI communicators and IO
   !--------------------------------------------------------------------------

   call mpi_init(ierr)
   call shr_mpi_chkerr(ierr,subname//' mpi_init')
 
   Global_Comm=MPI_COMM_WORLD
   call seq_io_init1(NLFileName, Global_Comm)

   if (Global_Comm /= MPI_COMM_NULL) then
!wangty modify
#ifdef wrf
        call seq_comm_init(Global_Comm, NLFileName, atm_petlist=atm_petlist, lnd_petlist=lnd_petlist, &
           ice_petlist=ice_petlist, ocn_petlist=ocn_petlist, glc_petlist=glc_petlist, &
           wrf_petlist=wrf_petlist, gea_petlist=gea_petlist) ! juanxiong he
#else
     call seq_comm_init(Global_Comm, NLFileName, atm_petlist=atm_petlist, lnd_petlist=lnd_petlist, &
          ice_petlist=ice_petlist, ocn_petlist=ocn_petlist, glc_petlist=glc_petlist)
#endif
   end if

   call seq_io_init2()
 
   !--- set task based threading counts ---
   call seq_comm_setptrs(GLOID,pethreads=pethreads_GLOID,iam=iam_GLOID)
   call seq_comm_setnthreads(pethreads_GLOID)

   !--- get some general data ---
   call seq_comm_setptrs(GLOID,mpicom=mpicom_GLOID,iamroot=iamroot_GLOID,nthreads=nthreads_GLOID)
   call seq_comm_setptrs(CPLID,mpicom=mpicom_CPLID,iamroot=iamroot_CPLID,nthreads=nthreads_CPLID)
   call seq_comm_setptrs(ATMID,mpicom=mpicom_ATMID,iamroot=iamroot_ATMID,nthreads=nthreads_ATMID)
   call seq_comm_setptrs(LNDID,mpicom=mpicom_LNDID,iamroot=iamroot_LNDID,nthreads=nthreads_LNDID)
   call seq_comm_setptrs(ICEID,mpicom=mpicom_ICEID,iamroot=iamroot_ICEID,nthreads=nthreads_ICEID)
   call seq_comm_setptrs(OCNID,mpicom=mpicom_OCNID,iamroot=iamroot_OCNID,nthreads=nthreads_OCNID)
   call seq_comm_setptrs(GLCID,mpicom=mpicom_GLCID,iamroot=iamroot_GLCID,nthreads=nthreads_GLCID)
!wangty modify
#ifdef wrf
   call seq_comm_setptrs(WRFID,mpicom=mpicom_WRFID,iamroot=iamroot_WRFID,nthreads=nthreads_WRFID) ! juanxiong he
   call seq_comm_setptrs(GEAID,mpicom=mpicom_GEAID,iamroot=iamroot_GEAID,nthreads=nthreads_GEAID) ! juanxiong he
#endif
   call seq_comm_setptrs(CPLATMID,mpicom=mpicom_CPLATMID,nthreads=nthreads_CPLATMID)
   call seq_comm_setptrs(CPLLNDID,mpicom=mpicom_CPLLNDID,nthreads=nthreads_CPLLNDID)
   call seq_comm_setptrs(CPLICEID,mpicom=mpicom_CPLICEID,nthreads=nthreads_CPLICEID)
   call seq_comm_setptrs(CPLOCNID,mpicom=mpicom_CPLOCNID,nthreads=nthreads_CPLOCNID)
   call seq_comm_setptrs(CPLGLCID,mpicom=mpicom_CPLGLCID,nthreads=nthreads_CPLGLCID)
!wangty modify
#ifdef wrf
   call seq_comm_setptrs(CPLWRFID,mpicom=mpicom_CPLWRFID,nthreads=nthreads_CPLWRFID) !juanxiong he
   call seq_comm_setptrs(CPLGEAID,mpicom=mpicom_CPLGEAID,nthreads=nthreads_CPLGEAID) !juanxiong he
#endif
   iamin_CPLID    = seq_comm_iamin(CPLID)
   iamin_ATMID    = seq_comm_iamin(ATMID)
   iamin_LNDID    = seq_comm_iamin(LNDID)
   iamin_ICEID    = seq_comm_iamin(ICEID)
   iamin_OCNID    = seq_comm_iamin(OCNID)
   iamin_GLCID    = seq_comm_iamin(GLCID)
!wangty modify
#ifdef wrf
   iamin_WRFID    = seq_comm_iamin(WRFID) ! juanxiong he
   iamin_GEAID    = seq_comm_iamin(GEAID) ! juanxiong he   
#endif
   iamin_CPLATMID = seq_comm_iamin(CPLATMID)
   iamin_CPLLNDID = seq_comm_iamin(CPLLNDID)
   iamin_CPLICEID = seq_comm_iamin(CPLICEID)
   iamin_CPLOCNID = seq_comm_iamin(CPLOCNID)
   iamin_CPLGLCID = seq_comm_iamin(CPLGLCID)
!wangty modify
#ifdef wrf
   iamin_CPLWRFID = seq_comm_iamin(CPLWRFID) !juanxiong he
   iamin_CPLGEAID = seq_comm_iamin(CPLGEAID) !juanxiong he
#endif
   complist = " "
   if (iamin_CPLID) complist = trim(complist)//' cpl'
   if (iamin_OCNID) complist = trim(complist)//' ocn'
   if (iamin_ATMID) complist = trim(complist)//' atm'
   if (iamin_LNDID) complist = trim(complist)//' lnd'
   if (iamin_ICEID) complist = trim(complist)//' ice'
   if (iamin_GLCID) complist = trim(complist)//' glc'
!wangty modify
#ifdef wrf
   if (iamin_WRFID) complist = trim(complist)//' wrf' !juanxiong he
   if (iamin_GEAID) complist = trim(complist)//' gea' !juanxiong he
#endif
   !--------------------------------------------------------------------------
   ! Set logging parameters both for shr code and locally
   !--------------------------------------------------------------------------

   if (iamroot_CPLID) then
	  CALL PUSH_MODULEID(MODULE_CPL)
      inquire(file='cpl_modelio.nml',exist=exists)      
      if (exists) then
         logunit = shr_file_getUnit()
         call shr_file_setIO('cpl_modelio.nml',logunit)
         call shr_file_setLogUnit(logunit)
         loglevel = 1
         call shr_file_setLogLevel(loglevel)
      endif
	  CALL POP_MODULEID()
   else
      loglevel = 0
      call shr_file_setLogLevel(loglevel)
   endif

   !--------------------------------------------------------------------------
   ! Log info about the environment settings
   !--------------------------------------------------------------------------

   if (iamroot_CPLID) then
#ifdef USE_ESMF_LIB
	  !CALL PUSH_MODULEID("iamroot_CPLID") 这一段导致多pop
      write(logunit,'(2A)') subname,' USE_ESMF_LIB is set'
#else
      write(logunit,'(2A)') subname,' USE_ESMF_LIB is NOT set, using esmf_wrf_timemgr'
#endif
#ifdef MCT_INTERFACE
      write(logunit,'(2A)') subname,' MCT_INTERFACE is set'
#endif
#ifdef ESMF_INTERFACE
      write(logunit,'(2A)') subname,' ESMF_INTERFACE is set'
#endif
	  !CALL POP_MODULEID()
   endif


end subroutine ccsm_pre_init

!-------------------------------------------------------------------------------
!
!-------------------------------------------------------------------------------

subroutine ccsm_init()

 101  format( A, 2i8, 12A, A, F8.2, A, F8.2 )
 102  format( A, 2i8, A, 5L3 )
 103  format( 5A )
 104  format( A, 2i8)
 105  format( A, 2i8, A, f10.2, A, f10.2, A, A, i5, A, A)
 106  format( A, f23.12)

   !--------------------------------------------------------------------------
   ! Print Model heading and copyright message
   !--------------------------------------------------------------------------

   if (iamroot_CPLID) call seq_ccsm_printlogheader()

   !-----------------------------------------------------------------------------
   ! Timer initialization (has to be after mpi init)
   !-----------------------------------------------------------------------------

   call t_initf(NLFileName, LogPrint=.false., mpicom=mpicom_GLOID, &
                MasterTask=iamroot_GLOID)

   if (iamin_CPLID) then
      call seq_io_cpl_init()
   endif

   call t_startf('DRIVER_INIT')

   !-----------------------------------------------------------------------------
   ! Memory test
   !-----------------------------------------------------------------------------
   call shr_mem_init(prt=.true.)

   !-----------------------------------------------------------------------------
   ! Initialize coupled field indices
   !-----------------------------------------------------------------------------

   call seq_flds_set()
   call seq_flds_indices_set( )

   !-----------------------------------------------------------------------------
   ! Initialize infodata
   !-----------------------------------------------------------------------------

   call seq_infodata_init(infodata,nlfilename,GLOID)
   if (iamroot_CPLID) then
      write(logunit,*) ' '
      write(logunit,'(2A)') 'Status of infodata after seq_infodata_init'
      call seq_infodata_print( infodata )
      write(logunit,*) ' '
   endif

   call seq_infodata_GetData(infodata,read_restart=read_restart, restart_file=rest_file, &
        timing_dir=timing_dir, tchkpt_dir=tchkpt_dir)
!wangty modify
#ifdef wrf
   call seq_infodata_GetData(infodata, info_debug=info_debug, atm_present=atm_present, &
        lnd_present=lnd_present, ice_present=ice_present, ocn_present=ocn_present, &
        glc_present=glc_present, sno_present=sno_present, wrf_present=wrf_present, & !juanxiong he
        geatm_present=geatm_present, & !juanxiong he
        single_column=single_column, aqua_planet=aqua_planet, &
        ocean_tight_coupling=ocean_tight_coupling, drv_threading=drv_threading)
#else
   call seq_infodata_GetData(infodata, info_debug=info_debug, atm_present=atm_present, &
        lnd_present=lnd_present, ice_present=ice_present, ocn_present=ocn_present, &
        glc_present=glc_present, sno_present=sno_present, &
        single_column=single_column, aqua_planet=aqua_planet, &
        ocean_tight_coupling=ocean_tight_coupling, drv_threading=drv_threading)
#endif
   call seq_infodata_GetData(infodata, do_histinit=do_histinit)
   call seq_infodata_GetData(infodata, do_budgets=do_budgets, budget_inst=budget_inst, &
        budget_daily=budget_daily, budget_month=budget_month, budget_ann=budget_ann, &
        budget_ltann=budget_ltann, budget_ltend=budget_ltend)
   call seq_infodata_GetData(infodata, &
        histaux_a2x    =do_hist_a2x    , histaux_a2x3hr =do_hist_a2x3hr , &
        histaux_a2x3hrp=do_hist_a2x3hrp, histaux_a2x24hr=do_hist_a2x24hr, &
        histaux_l2x    =do_hist_l2x    , histaux_r2x    =do_hist_r2x      )
   call seq_infodata_GetData(infodata, run_barriers = run_barriers)

   call seq_infodata_GetData(infodata, aoflux_grid=aoflux_grid)

   call seq_infodata_GetData(infodata, shr_map_dopole=shr_map_dopole)
   call shr_map_setDopole(shr_map_dopole)

   !-----------------------------------------------------------------------------
   ! Test Threading Setup in driver, happens to be valid on all pes for all IDs
   !-----------------------------------------------------------------------------

   if (drv_threading) then
      if (iamroot_GLOID) write(logunit,*) ' '
      if (iamroot_GLOID) write(logunit,'(2A)    ') subname,' Test Threading in driver'
      call seq_comm_setnthreads(nthreads_GLOID)
      if (iamroot_GLOID) write(logunit,'(2A,2I4)') subname,'    nthreads_GLOID = ',nthreads_GLOID,seq_comm_getnthreads()
      call seq_comm_setnthreads(nthreads_CPLID)
      if (iamroot_GLOID) write(logunit,'(2A,2I4)') subname,'    nthreads_CPLID = ',nthreads_CPLID,seq_comm_getnthreads()
      call seq_comm_setnthreads(nthreads_ATMID)
      if (iamroot_GLOID) write(logunit,'(2A,2I4)') subname,'    nthreads_ATMID = ',nthreads_ATMID,seq_comm_getnthreads()
      call seq_comm_setnthreads(nthreads_LNDID)
      if (iamroot_GLOID) write(logunit,'(2A,2I4)') subname,'    nthreads_LNDID = ',nthreads_LNDID,seq_comm_getnthreads()
      call seq_comm_setnthreads(nthreads_OCNID)
      if (iamroot_GLOID) write(logunit,'(2A,2I4)') subname,'    nthreads_OCNID = ',nthreads_OCNID,seq_comm_getnthreads()
      call seq_comm_setnthreads(nthreads_ICEID)
      if (iamroot_GLOID) write(logunit,'(2A,2I4)') subname,'    nthreads_ICEID = ',nthreads_ICEID,seq_comm_getnthreads()
      if (iamroot_GLOID) write(logunit,*) ' '
      call seq_comm_setnthreads(nthreads_GLCID)
      if (iamroot_GLOID) write(logunit,'(2A,2I4)') subname,'    nthreads_GLCID = ',nthreads_GLCID,seq_comm_getnthreads()
      if (iamroot_GLOID) write(logunit,*) ' '
!wangty modify
#ifdef wrf
      call seq_comm_setnthreads(nthreads_WRFID) ! juanxiong he
      if (iamroot_GLOID) write(logunit,'(2A,2I4)') subname,'    nthreads_WRFID = ',nthreads_WRFID,seq_comm_getnthreads()
      if (iamroot_GLOID) write(logunit,*)
      call seq_comm_setnthreads(nthreads_GEAID) ! juanxiong he
      if (iamroot_GLOID) write(logunit,'(2A,2I4)') subname,'    nthreads_GEAID =',nthreads_GEAID,seq_comm_getnthreads()
      if (iamroot_GLOID) write(logunit,*)
#endif
      call seq_comm_setnthreads(nthreads_GLOID)
   endif

   !-----------------------------------------------------------------------------
   ! Setup cdata types, call on all pes so the ID is set on all pes even 
   ! though other data may be invalid
   !-----------------------------------------------------------------------------

   call seq_cdata_init(cdata_ax, CPLID, dom_ax, gsMap_ax, infodata, 'cdata_ax' )
   call seq_cdata_init(cdata_lx, CPLID, dom_lx, gsMap_lx, infodata, 'cdata_lx' )
   call seq_cdata_init(cdata_rx, CPLID, dom_rx, gsMap_rx, infodata, 'cdata_rx' )
   call seq_cdata_init(cdata_ix, CPLID, dom_ix, gsMap_ix, infodata, 'cdata_ix' )
   call seq_cdata_init(cdata_ox, CPLID, dom_ox, gsMap_ox, infodata, 'cdata_ox' )
   call seq_cdata_init(cdata_gx, CPLID, dom_gx, gsMap_gx, infodata, 'cdata_gx' )
   call seq_cdata_init(cdata_sx, CPLID, dom_sx, gsMap_sx, infodata, 'cdata_sx' )
!wangty modify
#ifdef wrf
   call seq_cdata_init(cdata_wx, CPLID, dom_wx, gsMap_wx, infodata, 'cdata_wx' ) !juanxiong he, wrf/ccsm4 coupling
   call seq_cdata_init(cdata_mx, CPLID, dom_mx, gsMap_mx, infodata, 'cdata_mx' ) !juanxiong he, wrf/cam coupling, wrf end
   call seq_cdata_init(cdata_cx, CPLID, dom_cx, gsMap_cx, infodata, 'cdata_cx' ) !juanxiong he, wrf/cam coupling, cam end
   call seq_cdata_init(cdata_gex, CPLID, dom_gex, gsMap_gex, infodata, 'cdata_gex' )  !juanxiong he, geatm/ccsm4 coupling
   call seq_cdata_init(cdata_cax, CPLID, dom_cax, gsMap_cax, infodata, 'cdata_cax' )  !juanxiong he, geatm/cam coupling, cam end
#endif

   call seq_cdata_init(cdata_aa, ATMID, dom_aa, gsMap_aa, infodata, 'cdata_aa')
   call seq_cdata_init(cdata_ll, LNDID, dom_ll, gsMap_ll, infodata, 'cdata_ll')
   call seq_cdata_init(cdata_rr, LNDID, dom_rr, gsMap_rr, infodata, 'cdata_rr')
   call seq_cdata_init(cdata_ss, LNDID, dom_ss, gsMap_ss, infodata, 'cdata_ss')
   call seq_cdata_init(cdata_ii, ICEID, dom_ii, gsMap_ii, infodata, 'cdata_ii')
   call seq_cdata_init(cdata_oo, OCNID, dom_oo, gsMap_oo, infodata, 'cdata_oo')
   call seq_cdata_init(cdata_gg, GLCID, dom_gg, gsMap_gg, infodata, 'cdata_gg')
!wangty modify
#ifdef wrf
   call seq_cdata_init(cdata_ww, WRFID, dom_ww, gsMap_ww, infodata, 'cdata_ww' ) !juanxiong he, wrf/ccsm4 coupling
   call seq_cdata_init(cdata_mm, WRFID, dom_mm, gsMap_mm, infodata, 'cdata_mm' ) !juanxiong he, wrf/cam coupling, wrf end
   call seq_cdata_init(cdata_cc, ATMID, dom_cc, gsMap_cc, infodata, 'cdata_cc' ) !juanxiong he, wrf/cam coupling, cam end
   call seq_cdata_init(cdata_gege, GEAID, dom_gege, gsMap_gege, infodata, 'cdata_gege' )   !juanxiong he, geatm/cam coupling, geatm end
   call seq_cdata_init(cdata_caca, ATMID, dom_caca, gsMap_caca, infodata, 'cdata_caca' )   !juanxiong he, geatm/cam coupling, cam end
#endif
   !-----------------------------------------------------------------------------
   ! Initialize time manager
   !-----------------------------------------------------------------------------
!wangty modify
#ifdef wrf
   call seq_timemgr_clockInit(seq_SyncClock,nlfilename,read_restart,rest_file,mpicom_gloid, &
      EClock_d, EClock_a, EClock_l, EClock_o, EClock_i, Eclock_g, Eclock_w, Eclock_ge)  ! juanxiong he for wrf/ccsm4 coupling   
#else
   call seq_timemgr_clockInit(seq_SyncClock,nlfilename,read_restart,rest_file,mpicom_gloid, &
      EClock_d, EClock_a, EClock_l, EClock_o, EClock_i, Eclock_g)
#endif
   if (iamroot_CPLID) then
       call seq_timemgr_clockPrint(seq_SyncClock)
   endif

   call seq_infodata_getData(infodata,orb_iyear=orb_iyear,orb_iyear_align=orb_iyear_align, &
      orb_mode=orb_mode)
   if (trim(orb_mode) == trim(seq_infodata_orb_variable_year)) then
      call seq_timemgr_EClockGetData( EClock_d, curr_ymd=ymd)
      call shr_cal_date2ymd(ymd,year,month,day)
      orb_cyear = orb_iyear + (year - orb_iyear_align)
      call shr_orb_params(orb_cyear, orb_eccen, orb_obliq, orb_mvelp, &
                          orb_obliqr, orb_lambm0, orb_mvelpp, iamroot_CPLID)
      call seq_infodata_putData(infodata,orb_eccen=orb_eccen,orb_obliqr=orb_obliqr, &
           orb_lambm0=orb_lambm0,orb_mvelpp=orb_mvelpp)
   endif
!wangty modify
#ifdef wrf
   call seq_infodata_putData(infodata,atm_phase=1,lnd_phase=1,ocn_phase=1,ice_phase=1,glc_phase=1,&
                             wrf_phase=1, geatm_phase=1) !juanxiong he
#else
   call seq_infodata_putData(infodata,atm_phase=1,lnd_phase=1,ocn_phase=1,ice_phase=1,glc_phase=1)
#endif
   !-----------------------------------------------------------------------------
   ! If in single column mode overwrite lnd,ocn,ice_present flags according to 
   ! focndomain file in ocn_in namelist
   ! SCAM can reset the lnd_present, ice_present and ocn_present flags
   !-----------------------------------------------------------------------------

   if (.not.aqua_planet .and. single_column) then
      call seq_infodata_getData( infodata, scmlon=scmlon, scmlat=scmlat)
      call shr_scam_checkSurface(scmlon, scmlat, OCNID, mpicom_OCNID, &
           lnd_present=lnd_present, ice_present=ice_present, ocn_present=ocn_present)
      call seq_infodata_putData( infodata, &
           lnd_present=lnd_present, ocn_present=ocn_present, ice_present=ocn_present)
   endif

   !-----------------------------------------------------------------------------
   ! Component Initialization
   ! Note that within each component initialization, the relevant x_pxresent flag 
   ! part of CCSMInit (contained as a pointer in cdata_xc) can be modified
   ! By default, all these flags are set to true
   ! The atm can reset the lnd_present, ice_present and ocn_present flags based
   ! on aqua_planet, ideal_phys and adiabatic modes
   ! The stub components will reset the present flags to false, all other
   ! components will set them to true for the purposes of symmetry
   !-----------------------------------------------------------------------------

   call t_startf('driver_init_comps')
   if ( iamroot_CPLID )then
      write(logunit,*) ' '
!wangty modify
#ifdef wrf
      write(logunit,F00) 'Initialize each component: atm, wrf, gea, lnd, ocn, and ice' ! juanxiong he
#else
      write(logunit,F00) 'Initialize each component: atm, lnd, ocn, and ice'
#endif
      call shr_sys_flush(logunit)
   endif

   !-----------------------------------------------------------------------------
   ! Initialization atmospheric component
   !-----------------------------------------------------------------------------

   call t_adj_detailf(+2)

   if (iamin_CPLATMID) then
      call seq_infodata_exchange(infodata,CPLATMID,'cpl2atm_init')
   endif
   if (iamin_ATMID .and. atm_present) then
      if (seq_comm_iamroot(ATMID)) write(logunit,F00) 'Initialize atm component'
      call shr_sys_flush(logunit)
      if (drv_threading) call seq_comm_setnthreads(nthreads_ATMID)
!wangty modify
#ifdef wrf
      call atm_init_mct( EClock_a, cdata_aa, cdata_cc, cdata_caca, x2a_aa, a2x_aa, &
                         x2c_cc1, x2c_cc2, c2x_cc1, c2x_cc2, &  ! juanxiong he for wrf
                         x2ca_caca1, x2ca_caca2, ca2x_caca1, ca2x_caca2, & ! juanxiong he for geatm
                         twoway_coupling, twoway_nudging, NLFilename=NLFilename ) !juanxiong he
#else
      call atm_init_mct( EClock_a, cdata_aa, x2a_aa, a2x_aa, NLFilename=NLFilename )
#endif

      if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
   endif
   if (iamin_CPLATMID) then
      call seq_infodata_exchange(infodata,CPLATMID,'atm2cpl_init')
   endif
!wangty modify
#ifdef wrf
   !-----------------------------------------------------------------------------
   ! Initialization WRF component, juanxiong he
   !-----------------------------------------------------------------------------
   if (iamin_CPLWRFID) then
      call seq_infodata_exchange(infodata,CPLWRFID,'cpl2wrf_init')
   endif
   if (iamin_WRFID .and. wrf_present) then
      if (seq_comm_iamroot(WRFID)) write(logunit,F00) 'Initialize wrf component'
      call shr_sys_flush(logunit)
      if (drv_threading) call seq_comm_setnthreads(nthreads_WRFID)
      call wrf_init_mct( EClock_w, cdata_ww, cdata_mm, x2w_ww, w2x_ww, x2m_mm1, x2m_mm2, &
                         m2x_mm, twoway_coupling, twoway_nudging, NLFilename=NLFilename )
      if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
   endif
   if (iamin_CPLWRFID) then
      call seq_infodata_exchange(infodata,CPLWRFID,'wrf2cpl_init')
   endif

   !-----------------------------------------------------------------------------
   ! Initialization GEATM component, juanxiong he
   !-----------------------------------------------------------------------------

   if (iamin_CPLGEAID) then
      call seq_infodata_exchange(infodata,CPLGEAID,'cpl2gea_init')
   endif
   if (iamin_GEAID .and. geatm_present) then
      if (seq_comm_iamroot(GEAID)) write(logunit,F00) 'Initialize gea component'
      call shr_sys_flush(logunit)
      if (drv_threading) call seq_comm_setnthreads(nthreads_GEAID)
      call geatm_init_mct( EClock_ge, cdata_gege, &
                           x2chem_chemchem1,x2chem_chemchem2, chem2x_chemchem )
      if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
   endif
   if (iamin_CPLGEAID) then
      call seq_infodata_exchange(infodata,CPLGEAID,'gea2cpl_init')
   endif
#endif
   !-----------------------------------------------------------------------------
   ! Initialization land component
   !-----------------------------------------------------------------------------

   if (iamin_CPLLNDID) then
      call seq_infodata_exchange(infodata,CPLLNDID,'cpl2lnd_init')
   endif
   if (iamin_LNDID .and. lnd_present) then
      if (drv_threading) call seq_comm_setnthreads(nthreads_LNDID)
      if (seq_comm_iamroot(LNDID)) write(logunit,F00) 'Initialize lnd component'
      call shr_sys_flush(logunit)
      call lnd_init_mct( EClock_l, cdata_ll, x2l_ll, l2x_ll, &
                                   cdata_rr,         r2x_rr, &
                                   cdata_ss, x2s_ss, s2x_ss, NLFilename=NLFilename )
      if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
    endif
   if (iamin_CPLLNDID) then
      call seq_infodata_exchange(infodata,CPLLNDID,'lnd2cpl_init')
   endif

   !-----------------------------------------------------------------------------
   ! Initialization ocean component
   !-----------------------------------------------------------------------------

   if (iamin_CPLOCNID) then
      call seq_infodata_exchange(infodata,CPLOCNID,'cpl2ocn_init')
   endif
   if (iamin_OCNID .and. ocn_present) then
      if (drv_threading) call seq_comm_setnthreads(nthreads_OCNID)
      if (seq_comm_iamroot(OCNID)) write(logunit,F00) 'Initialize ocn component'
      call shr_sys_flush(logunit)
      call ocn_init_mct( EClock_o, cdata_oo, x2o_oo, o2x_oo, NLFilename=NLFilename )
      if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
   endif
   if (iamin_CPLOCNID) then
      call seq_infodata_exchange(infodata,CPLOCNID,'ocn2cpl_init')
   endif

   !-----------------------------------------------------------------------------
   ! Initialization ice component
   !-----------------------------------------------------------------------------

   if (iamin_CPLICEID) then
      call seq_infodata_exchange(infodata,CPLICEID,'cpl2ice_init')
   endif
   if (iamin_ICEID .and. ice_present) then
      if (drv_threading) call seq_comm_setnthreads(nthreads_ICEID)
      if (seq_comm_iamroot(ICEID)) write(logunit,F00) 'Initialize ice component'
      call shr_sys_flush(logunit)
      call ice_init_mct( EClock_i, cdata_ii, x2i_ii, i2x_ii, NLFilename=NLFilename )
      if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
   endif
   if (iamin_CPLICEID) then
      call seq_infodata_exchange(infodata,CPLICEID,'ice2cpl_init')
   endif

   !-----------------------------------------------------------------------------
   ! Initialization glc component
   !-----------------------------------------------------------------------------

   if (iamin_CPLGLCID) then
      call seq_infodata_exchange(infodata,CPLGLCID,'cpl2glc_init')
   endif
   if (iamin_GLCID .and. glc_present) then
      if (drv_threading) call seq_comm_setnthreads(nthreads_GLCID)
      if (seq_comm_iamroot(GLCID)) write(logunit,F00) 'Initialize glc component'
      call shr_sys_flush(logunit)
      call glc_init_mct( EClock_g, cdata_gg, x2g_gg, g2x_gg, NLFilename=NLFilename )
      if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
   endif
   if (iamin_CPLGLCID) then
      call seq_infodata_exchange(infodata,CPLGLCID,'glc2cpl_init')
   endif

   call t_adj_detailf(-2)

   call t_stopf  ('driver_init_comps')

   !-----------------------------------------------------------------------------
   ! Determine final settings for presence of land, ice and ocean and the prognostic flags
   !-----------------------------------------------------------------------------

   if (iamin_CPLATMID) then
      call seq_infodata_exchange(infodata,CPLATMID,'cpl2atm_init')
   endif
!wangty modify
#ifdef wrf
   if (iamin_CPLWRFID) then  !juanxiong he
      call seq_infodata_exchange(infodata,CPLWRFID,'cpl2wrf_init')
   endif
   if (iamin_CPLGEAID) then  !juanxiong he
      call seq_infodata_exchange(infodata,CPLGEAID,'cpl2gea_init')
   endif  
#endif 
   if (iamin_CPLLNDID) then
      call seq_infodata_exchange(infodata,CPLLNDID,'cpl2lnd_init')
   endif
   if (iamin_CPLOCNID) then
      call seq_infodata_exchange(infodata,CPLOCNID,'cpl2ocn_init')
   endif
   if (iamin_CPLICEID) then
      call seq_infodata_exchange(infodata,CPLICEID,'cpl2ice_init')
   endif
   if (iamin_CPLGLCID) then
      call seq_infodata_exchange(infodata,CPLGLCID,'cpl2glc_init')
   endif

   if ( iamroot_CPLID) then
      write(logunit,F00) 'Determine final settings for presence of surface components'
      call shr_sys_flush(logunit)
   endif

   call seq_infodata_getData(infodata, &
        atm_present=atm_present, &
!wangty modify
#ifdef wrf
        wrf_present=wrf_present, & !juaxniong he
        geatm_present=geatm_present, & !juaxniong he
#endif
        lnd_present=lnd_present, &
        rof_present=rof_present, &
        ice_present=ice_present, &
        ocn_present=ocn_present, & 
        glc_present=glc_present, & 
        sno_present=sno_present, & 
        atm_prognostic=atm_prognostic, &
!wangty modify
#ifdef wrf
        wrf_prognostic=wrf_prognostic, & !juanxiong he
        geatm_prognostic=geatm_prognostic, & !juanxiong he
#endif
        lnd_prognostic=lnd_prognostic, &
        ice_prognostic=ice_prognostic, &
        ocn_prognostic=ocn_prognostic, &
        ocnrof_prognostic=ocnrof_prognostic, &
        glc_prognostic=glc_prognostic, &
        sno_prognostic=sno_prognostic, &
        dead_comps=dead_comps, &
        atm_nx=atm_nx, atm_ny=atm_ny, &
!wangty modify
#ifdef wrf
        wrf_nx=wrf_nx, wrf_ny=wrf_ny, & ! juanxiong he
        geatm_nx=geatm_nx, geatm_ny=geatm_ny, & ! juanxiong he         
#endif
        lnd_nx=lnd_nx, lnd_ny=lnd_ny, &
        rof_nx=rof_nx, rof_ny=rof_ny, &
        ice_nx=ice_nx, ice_ny=ice_ny, &
        glc_nx=glc_nx, glc_ny=glc_ny, &
        sno_nx=sno_nx, sno_ny=sno_ny, &
        ocn_nx=ocn_nx, ocn_ny=ocn_ny, &
        cpl_cdf64=cdf64, &
        atm_aero=atm_aero )

   if (.not. atm_present) then
      call shr_sys_abort('atm must be present')
   endif
   if (ocnrof_prognostic .and. .not.rof_present) then
      if (iamroot_CPLID) then
         write(logunit,F00) 'WARNING: ocnrof_prognostic is TRUE but rof_present is FALSE'
         call shr_sys_flush(logunit)
      endif
   endif
   if (ocn_prognostic .and. .not.ocn_present) then
      call shr_sys_abort('if prognostic ocn must also have ocn present')
   endif
   if (lnd_prognostic .and. .not.lnd_present) then
      call shr_sys_abort('if prognostic lnd must also have lnd present')
   endif
   if (ice_prognostic .and. .not.ice_present) then
      call shr_sys_abort('if prognostic ice must also have ice present')
   endif
   if (glc_prognostic .and. .not.glc_present) then
      call shr_sys_abort('if prognostic glc must also have glc present')
   endif
   if (sno_prognostic .and. .not.sno_present) then
      call shr_sys_abort('if prognostic sno must also have sno present')
   endif
!wangty modify
#ifdef wrf
   if (wrf_prognostic .and. .not.wrf_present) then  !juanxiong he
      call shr_sys_abort('if prognostic wrf must also have wrf present')
   endif
   if (geatm_prognostic .and. .not.geatm_present) then  !juanxiong he
      call shr_sys_abort('if prognostic geatm must also have geatm present')
   endif
#endif
! tcx remove temporarily for development
!   if (glc_prognostic .and. .not.sno_present) then
!      call shr_sys_abort('if prognostic glc must also have sno present')
!   endif
!   if (sno_prognostic .and. .not.glc_present) then
!      call shr_sys_abort('if prognostic sno must also have glc present')
!   endif

   !-----------------------------------------------------------------------------
   ! Set domain check and other flag
   !-----------------------------------------------------------------------------

   domain_check = .true.
   if (single_column         ) domain_check = .false.
   if (dead_comps            ) domain_check = .false.

   ! set skip_ocean_run flag, used primarily for ocn run on first timestep
   ! use reading a restart as a surrogate from whether this is a startup run

   skip_ocean_run = .true.
   if ( read_restart) skip_ocean_run = .false.
   ocnrun_count = 0
   cpl2ocn_first = .true.

   do_histavg = .true.
   if (seq_timemgr_histavg_type == seq_timemgr_type_never) then
      do_histavg = .false.
   endif

   !-----------------------------------------------------------------------------
   ! Write output
   ! NOTE- assume that runoff will only be mapped from land to ocean if 
   !       prognostic ocean is true
   !-----------------------------------------------------------------------------

   if (iamroot_CPLID) then
      write(logunit,*  )' '
      write(logunit,F00)'After component initialization:'
      write(logunit,F0L)'atm model present     = ',atm_present
!wangty modify
#ifdef wrf
      write(logunit,F0L)'wrf model present     = ',wrf_present ! juanxiong he
      write(logunit,F0L)'geatm  model present  = ',geatm_present ! juanxiong he      
#endif
      write(logunit,F0L)'lnd model present     = ',lnd_present
      write(logunit,F0L)'ocn model present     = ',ocn_present
      write(logunit,F0L)'ice model present     = ',ice_present
      write(logunit,F0L)'glc model present     = ',glc_present
      write(logunit,F0L)'sno model present     = ',sno_present
      write(logunit,F0L)'atm model prognostic  = ',atm_prognostic
!wangty modify
#ifdef wrf
      write(logunit,F0L)'wrf model prognostic  = ',wrf_prognostic ! juanxiong he
      write(logunit,F0L)'geatm model prognostic  = ',geatm_prognostic ! juanxiong he
#endif
      write(logunit,F0L)'lnd model prognostic  = ',lnd_prognostic
      write(logunit,F0L)'ocn model prognostic  = ',ocn_prognostic
      write(logunit,F0L)'ice model prognostic  = ',ice_prognostic
      write(logunit,F0L)'glc model prognostic  = ',glc_prognostic
      write(logunit,F0L)'sno model prognostic  = ',sno_prognostic
      write(logunit,F0L)'lnd rof   present     = ',rof_present
      write(logunit,F0L)'ocn rof   prognostic  = ',ocnrof_prognostic
      write(logunit,F0L)'dead components       = ',dead_comps
      write(logunit,F0L)'domain_check          = ',domain_check
      write(logunit,F0I)'atm_nx,atm_ny         = ',atm_nx,atm_ny
!wangty modify
#ifdef wrf
      write(logunit,F0I)'wrf_nx,wrf_ny         = ',wrf_nx,wrf_ny !juanxiong he
      write(logunit,F0I)'geatm_nx,geatm_ny         = ',geatm_nx,geatm_ny !juanxiong he
#endif
      write(logunit,F0I)'lnd_nx,lnd_ny         = ',lnd_nx,lnd_ny
      write(logunit,F0I)'rof_nx,rof_ny         = ',rof_nx,rof_ny
      write(logunit,F0I)'ice_nx,ice_ny         = ',ice_nx,ice_ny
      write(logunit,F0I)'ocn_nx,ocn_ny         = ',ocn_nx,ocn_ny
      write(logunit,F0I)'glc_nx,glc_ny         = ',glc_nx,glc_ny
      write(logunit,F0I)'sno_nx,sno_ny         = ',sno_nx,sno_ny
      write(logunit,F0L)'skip init ocean run   = ',skip_ocean_run
      write(logunit,F0L)'ocean tight coupling  = ',ocean_tight_coupling
      write(logunit,F0L)'cpl_cdf64             = ',cdf64
      write(logunit,F0L)'do_histavg            = ',do_histavg
      write(logunit,F0L)'atm_aero              = ',atm_aero
      write(logunit,*  )' '
      call shr_sys_flush(logunit)
   endif

   !-----------------------------------------------------------------------------
   ! Need to initialize aream, set it to area for now until maps are read
   !   in some cases, maps are not read at all !!
   ! Need to initialize ascale
   ! Entire domain must have reasonable values before calling xxx2xxx init
   ! NOTE (tcx) : use cdata%dom instead of dom% due to seg fault on bluevista I, why?
   !-----------------------------------------------------------------------------

   if (iamin_ATMID .and. atm_present) then
      if (drv_threading) call seq_comm_setnthreads(nthreads_ATMID)
      k1 = mct_aVect_indexRa(cdata_aa%dom%data,"area"  ,perrWith='aa area ')
      k2 = mct_aVect_indexRa(cdata_aa%dom%data,"aream" ,perrWith='aa aream')
      k3 = mct_aVect_indexRa(cdata_aa%dom%data,"ascale",perrWith='aa ascale')
      cdata_aa%dom%data%rAttr(k2,:) = cdata_aa%dom%data%rAttr(k1,:)
      cdata_aa%dom%data%rAttr(k3,:) = 1.0_r8
      if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
   endif

   if (iamin_LNDID .and. lnd_present) then
      if (drv_threading) call seq_comm_setnthreads(nthreads_LNDID)
      k1 = mct_aVect_indexRa(cdata_ll%dom%data,"area"  ,perrWith='ll area ')
      k2 = mct_aVect_indexRa(cdata_ll%dom%data,"aream" ,perrWith='ll aream')
      k3 = mct_aVect_indexRa(cdata_ll%dom%data,"ascale",perrWith='ll ascale')
      cdata_ll%dom%data%rAttr(k2,:) = cdata_ll%dom%data%rAttr(k1,:)
      cdata_ll%dom%data%rAttr(k3,:) = 1.0_r8
      if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
   endif

   if (iamin_LNDID .and. rof_present) then
      if (drv_threading) call seq_comm_setnthreads(nthreads_LNDID)
      k1 = mct_aVect_indexRa(cdata_rr%dom%data,"area"  ,perrWith='rr area ')
      k2 = mct_aVect_indexRa(cdata_rr%dom%data,"aream" ,perrWith='rr aream')
      k3 = mct_aVect_indexRa(cdata_rr%dom%data,"ascale",perrWith='rr ascale')
      cdata_rr%dom%data%rAttr(k2,:) = cdata_rr%dom%data%rAttr(k1,:)
      cdata_rr%dom%data%rAttr(k3,:) = 1.0_r8
      if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
   endif

   if (iamin_LNDID .and. sno_present) then
      if (drv_threading) call seq_comm_setnthreads(nthreads_LNDID)
      k1 = mct_aVect_indexRa(cdata_ss%dom%data,"area"  ,perrWith='ss area ')
      k2 = mct_aVect_indexRa(cdata_ss%dom%data,"aream" ,perrWith='ss aream')
      k3 = mct_aVect_indexRa(cdata_ss%dom%data,"ascale",perrWith='ss ascale')
      cdata_ss%dom%data%rAttr(k2,:) = cdata_ss%dom%data%rAttr(k1,:)
      cdata_ss%dom%data%rAttr(k3,:) = 1.0_r8
      if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
   endif

   if (iamin_OCNID .and. ocn_present) then
      if (drv_threading) call seq_comm_setnthreads(nthreads_OCNID)
      k1 = mct_aVect_indexRa(cdata_oo%dom%data,"area"  ,perrWith='oo area ')
      k2 = mct_aVect_indexRa(cdata_oo%dom%data,"aream" ,perrWith='oo aream')
      k3 = mct_aVect_indexRa(cdata_oo%dom%data,"ascale",perrWith='oo ascale')
      cdata_oo%dom%data%rAttr(k2,:) = cdata_oo%dom%data%rAttr(k1,:)
      cdata_oo%dom%data%rAttr(k3,:) = 1.0_r8
      if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
   endif

   if (iamin_ICEID .and. ice_present) then
      if (drv_threading) call seq_comm_setnthreads(nthreads_ICEID)
      k1 = mct_aVect_indexRa(cdata_ii%dom%data,"area"  ,perrWith='ii area ')
      k2 = mct_aVect_indexRa(cdata_ii%dom%data,"aream" ,perrWith='ii aream')
      k3 = mct_aVect_indexRa(cdata_ii%dom%data,"ascale",perrWith='ii ascale')
      cdata_ii%dom%data%rAttr(k2,:) = cdata_ii%dom%data%rAttr(k1,:)
      cdata_ii%dom%data%rAttr(k3,:) = 1.0_r8
      if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
   endif

   if (iamin_GLCID .and. glc_present) then
      if (drv_threading) call seq_comm_setnthreads(nthreads_GLCID)
      k1 = mct_aVect_indexRa(cdata_gg%dom%data,"area"  ,perrWith='gg area ')
      k2 = mct_aVect_indexRa(cdata_gg%dom%data,"aream" ,perrWith='gg aream')
      k3 = mct_aVect_indexRa(cdata_gg%dom%data,"ascale",perrWith='gg ascale')
      cdata_gg%dom%data%rAttr(k2,:) = cdata_gg%dom%data%rAttr(k1,:)
      cdata_gg%dom%data%rAttr(k3,:) = 1.0_r8
      if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
   endif

   !-----------------------------------------------------------------------------
   ! Initialize driver rearrangers and AVs on driver
   ! Initialize cdata_*x data
   ! Zero out x2*_** in case it never gets used then it'll produce zeros in diags
   !-----------------------------------------------------------------------------
   call t_startf('driver_init_xxx2xxx')

   if (iamin_CPLATMID .and. atm_present) then
      call map_atm2atm_init_mct(cdata_aa, x2a_aa, a2x_aa, ATMID, &
                                cdata_ax, x2a_ax, a2x_ax, CPLID, CPLATMID)
      call mct_avect_zero(x2a_aa)
      call map_atma2atmx_mct(cdata_aa, x2a_aa, cdata_ax, x2a_ax)
   endif

   if (iamin_CPLLNDID .and. lnd_present) then
      call map_lnd2lnd_init_mct(cdata_ll, x2l_ll, l2x_ll, LNDID, &
                                cdata_lx, x2l_lx, l2x_lx, CPLID, CPLLNDID)
      call mct_avect_zero(x2l_ll)
      call map_lndl2lndx_mct(cdata_ll, x2l_ll, cdata_lx, x2l_lx)
   endif

   if (iamin_CPLLNDID .and. rof_present) then
      call map_rof2rof_init_mct(cdata_rr,         r2x_rr, LNDID, &
                                cdata_rx,         r2x_rx, CPLID, CPLLNDID)
      call mct_avect_init(r2xacc_rx%data, r2x_rx, mct_aVect_lsize(r2x_rx))
      call mct_accum_zero(r2xacc_rx)
      r2xacc_rx_cnt = 0
   endif

   if (iamin_CPLLNDID .and. sno_present) then
      call map_sno2sno_init_mct(cdata_ss, x2s_ss, s2x_ss, LNDID, &
                                cdata_sx, x2s_sx, s2x_sx, CPLID, CPLLNDID)
      call mct_avect_zero(x2s_ss)
      call map_snos2snox_mct(cdata_ss, x2s_ss, cdata_sx, x2s_sx)
   endif

   if (iamin_CPLICEID .and. ice_present) then
      call map_ice2ice_init_mct(cdata_ii, x2i_ii, i2x_ii, ICEID, &
                                cdata_ix, x2i_ix, i2x_ix, CPLID, CPLICEID)
      call mct_avect_zero(x2i_ii)
      call map_icei2icex_mct(cdata_ii, x2i_ii, cdata_ix, x2i_ix)
   endif

   if (iamin_CPLGLCID .and. glc_present) then
      call map_glc2glc_init_mct(cdata_gg, x2g_gg, g2x_gg, GLCID, &
                                cdata_gx, x2g_gx, g2x_gx, CPLID, CPLGLCID)
      call mct_avect_zero(x2g_gg)
      call map_glcg2glcx_mct(cdata_gg, x2g_gg, cdata_gx, x2g_gx)
   endif

   if (iamin_CPLOCNID .and. ocn_present) then
      call map_ocn2ocn_init_mct(cdata_oo, x2o_oo, o2x_oo, OCNID, &
                                cdata_ox, x2o_ox, o2x_ox, CPLID, CPLOCNID)
      call mct_avect_zero(x2o_oo)
      call map_ocno2ocnx_mct(cdata_oo, x2o_oo, cdata_ox, x2o_ox)
!      call mct_accum_init(x2oacc_ox, x2o_ox)
      call mct_avect_init(x2oacc_ox%data, x2o_ox, mct_aVect_lsize(x2o_ox))
      call mct_accum_zero(x2oacc_ox)
      x2oacc_ox_cnt = 0
   endif
!wangty modify
#ifdef wrf
   !-----------------------------------------------------------------------------
   ! GEATM and WRF, Juanxiong He
   !-----------------------------------------------------------------------------

   if (iamin_CPLATMID .and. atm_present) then !juanxiong he, for wrf/cam coupling, cam import
      call map_cam2cam_init_mct(cdata_cc, x2c_cc1, c2x_cc1, ATMID, &
                                cdata_cx, x2c_cx1, c2x_cx1, CPLID, CPLATMID)
      call map_cam2cam_init_mct(cdata_cc, x2c_cc2, c2x_cc2, ATMID, &
                                cdata_cx, x2c_cx2, c2x_cx2, CPLID, CPLATMID)
      call mct_avect_zero(x2c_cc1)
      call mct_avect_zero(x2c_cc2)
      call map_cama2camx_mct(cdata_cc, x2c_cc1, cdata_cx, x2c_cx1)  ! obviously, cam doesn't need data from wrf to drive its run
      call map_cama2camx_mct(cdata_cc, x2c_cc2, cdata_cx, x2c_cx2)  ! obviously, cam doesn't need data from wrf to drive its run
   endif

   if (iamin_CPLWRFID .and. wrf_present) then !juanxiong he, for wrf/cam coupling, wrf import
      call map_wrf2wrf_init_mct(cdata_mm, x2m_mm1, m2x_mm, WRFID, &
                                cdata_mx, x2m_mx1, m2x_mx, CPLID, CPLWRFID)
      call map_wrf2wrf_init_mct(cdata_mm, x2m_mm2, m2x_mm, WRFID, &
                                cdata_mx, x2m_mx2, m2x_mx, CPLID, CPLWRFID)
      call mct_avect_zero(x2m_mm1)
      call mct_avect_zero(x2m_mm2)
      call map_wrfw2wrfx_mct(cdata_mm, x2m_mm1, cdata_mx, x2m_mx1)   ! prepare import
      call map_wrfw2wrfx_mct(cdata_mm, x2m_mm2, cdata_mx, x2m_mx2)   ! prepare import
   endif

   if (iamin_CPLATMID .and. atm_present) then !juanxiong he, for gea/cam coupling, cam import
      call map_gcam2cam_init_mct(cdata_caca, x2ca_caca1, ca2x_caca1, ATMID, &
                                 cdata_cax, x2ca_cax1, ca2x_cax1, CPLID, CPLATMID)
      call map_gcam2cam_init_mct(cdata_caca, x2ca_caca2, ca2x_caca2, ATMID, &
                                 cdata_cax, x2ca_cax2, ca2x_cax2, CPLID, CPLATMID)
      call mct_avect_zero(x2ca_caca1)
      call mct_avect_zero(x2ca_caca2)
      call map_gcama2camx_mct(cdata_caca, x2ca_caca1, cdata_cax, x2ca_cax1)
      call map_gcama2camx_mct(cdata_caca, x2ca_caca2, cdata_cax, x2ca_cax2)
   endif

   if (iamin_CPLGEAID .and. geatm_present) then !juanxiong he, for geatm/cam coupling, geatm import
      call map_gea2gea_init_mct(cdata_gege, x2chem_chemchem1, chem2x_chemchem, GEAID, &
                                cdata_gex, x2chem_chemx1, chem2x_chemx, CPLID, CPLGEAID)
      call map_gea2gea_init_mct(cdata_gege, x2chem_chemchem2, chem2x_chemchem, GEAID, &
                                cdata_gex, x2chem_chemx2, chem2x_chemx, CPLID, CPLGEAID)
      call mct_avect_zero(x2chem_chemchem1)
      call mct_avect_zero(x2chem_chemchem2)
      call map_geaw2geax_mct(cdata_gege, x2chem_chemchem1, cdata_gex, x2chem_chemx1)   ! prepare import
      call map_geaw2geax_mct(cdata_gege, x2chem_chemchem2, cdata_gex, x2chem_chemx2)   ! prepare import
   endif
   !-----------------------------------------------------------------------------
   ! GEATM and WRF, Juanxiong He
   !-----------------------------------------------------------------------------
#endif
   call t_stopf  ('driver_init_xxx2xxx')

   !-----------------------------------------------------------------------------
   ! Remainder of initialization
   !-----------------------------------------------------------------------------

   if (iamin_CPLID) then
      if (drv_threading) call seq_comm_setnthreads(nthreads_CPLID)

      !-----------------------------------------------------------------------------
      ! Allocate attribute vectors for merge components
      !-----------------------------------------------------------------------------

      if ( seq_comm_iamroot(CPLID)) write(logunit,F00) 'Initializing merge components'
                       call mrg_x2a_init_mct( cdata_ax, l2x_ax, o2x_ax, i2x_ax, xao_ax )
!wangty modify
#ifdef wrf
                       call mrg_x2w_init_mct( cdata_mx, c2x_mx1 )  !juanxiong he
                       call mrg_x2w_init_mct( cdata_mx, c2x_mx2 )  !juanxiong he
                       call mrg_x2c_init_mct( cdata_cx, m2x_cx )  !juanxiong he
                       call mrg_x2ge_init_mct( cdata_gex, ca2x_chemx1 ) !juanxiong he
                       call mrg_x2ge_init_mct( cdata_gex, ca2x_chemx2 ) !juanxiong he
                       call mrg_x2ca_init_mct( cdata_cax, chem2x_cax ) !juanxiong he      
#endif
      if (ice_present) call mrg_x2i_init_mct( cdata_ix, a2x_ix, o2x_ix )
      if (ocn_present) call mrg_x2o_init_mct( cdata_ox, a2x_ox, i2x_ox, r2x_ox )
      if (lnd_present) call mrg_x2l_init_mct( cdata_lx, a2x_lx) 
      if (glc_present) call mrg_x2g_init_mct( cdata_gx, s2x_gx)
      if (sno_present) call mrg_x2s_init_mct( cdata_sx, g2x_sx)

      !-----------------------------------------------------------------------------
      ! Initialize mapping
      ! Read aream into domains!
      !-----------------------------------------------------------------------------

      call t_startf('driver_init_maps')

      if (ocn_present) then
         if ( seq_comm_iamroot(CPLID)) write(logunit,F00) 'Initializing atm/ocn mapping'
         call map_atm2ocn_init_mct(cdata_ax, cdata_ox)
         call map_ocn2atm_init_mct(cdata_ox, cdata_ax)
      endif
      if (ice_present .and. ocn_present) then
         if ( seq_comm_iamroot(CPLID)) write(logunit,F00) 'Initializing ocn/ice mapping'
         call map_ocn2ice_init_mct(cdata_ox, cdata_ix)
         call map_ice2ocn_init_mct(cdata_ix, cdata_ox)
      endif
      if (ice_present) then
         if ( seq_comm_iamroot(CPLID)) write(logunit,F00) 'Initializing atm/ice mapping'
!         call map_atm2ice_init_mct(cdata_ax, cdata_ix)
         call map_ice2atm_init_mct(cdata_ix, cdata_ax)
      endif
      if (rof_present .and. ocnrof_prognostic) then
         if ( seq_comm_iamroot(CPLID)) write(logunit,F00) 'Initializing rof/ocn mapping'
         call map_rof2ocn_init_mct(cdata_rx, cdata_ox)
      endif
      if (lnd_present) then
         if ( seq_comm_iamroot(CPLID)) write(logunit,F00) 'Initializing atm/lnd mapping'
         call map_atm2lnd_init_mct(cdata_ax, cdata_lx)
         call map_lnd2atm_init_mct(cdata_lx, cdata_ax)
      endif
      if (sno_present .and. glc_present) then
         if ( seq_comm_iamroot(CPLID)) write(logunit,F00) 'Initializing sno/glc mapping'
         call map_sno2glc_init_mct(cdata_sx, cdata_gx)
         call map_glc2sno_init_mct(cdata_gx, cdata_sx)
      endif
!wangty modify
#ifdef wrf
      if (wrf_present) then     ! juanxiong he
         if ( seq_comm_iamroot(CPLID)) write(logunit,F00) 'Initializing wrf/cam mapping'
         call map_cam2wrf_init_mct(cdata_cx, cdata_mx)
         call map_wrf2cam_init_mct(cdata_mx, cdata_cx)
      endif
      if (geatm_present) then     ! juanxiong he
         if ( seq_comm_iamroot(CPLID)) write(logunit,F00) 'Initializing geatm/cam mapping'
         call map_cam2gea_init_mct(cdata_cax, cdata_gex)
         call map_gea2cam_init_mct(cdata_gex, cdata_cax)
      endif
#endif
      call t_stopf  ('driver_init_maps')

      !-----------------------------------------------------------------------------
      ! Check domains if appropriate
      ! This must be done after the mappers are initialized since
      ! checking is done on each processor and not with a global gather
      !-----------------------------------------------------------------------------

      if (domain_check) then
         if ( seq_comm_iamroot(CPLID)) write(logunit,F00) 'Performing domain checking'
         call seq_domain_check_mct( cdata_ax, cdata_ix, cdata_lx, cdata_ox, &
                                    cdata_rx, cdata_gx, cdata_sx)
      endif

      if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
   endif ! iamin_CPLID

   !-----------------------------------------------------------------------------
   ! Map  dom_*x to dom_** in case any domain fields have been updated on cpl pes
   ! Initialize area corrections based on aream (read in map_init) and area
   ! Area correct component initialization output fields
   ! Map initial component AVs from component to coupler pes
   !-----------------------------------------------------------------------------

   if (iamin_CPLATMID .and. atm_present) then
      call map_atmx2atma_mct( cdata_ax, dom_ax%data, cdata_aa, dom_aa%data)
      if (iamin_ATMID) then
         call domain_areafactinit_mct(cdata_aa,mdl2drv_aa,drv2mdl_aa,'areafact_a')
         call mct_avect_vecmult(a2x_aa,mdl2drv_aa,seq_flds_a2x_fluxes)
      endif
      call map_atma2atmx_mct(cdata_aa, a2x_aa, cdata_ax, a2x_ax)
   endif

   if (iamin_CPLLNDID .and. lnd_present) then
      call map_lndx2lndl_mct( cdata_lx, dom_lx%data, cdata_ll, dom_ll%data)
      if (iamin_LNDID) then
         call domain_areafactinit_mct(cdata_ll,mdl2drv_ll,drv2mdl_ll,'areafact_l')
         call mct_avect_vecmult(l2x_ll,mdl2drv_ll,seq_flds_l2x_fluxes)
      endif
      call map_lndl2lndx_mct(cdata_ll, l2x_ll, cdata_lx, l2x_lx)
   endif

   if (iamin_CPLLNDID .and. rof_present) then
      call map_rofx2rofr_mct( cdata_rx, dom_rx%data, cdata_rr, dom_rr%data)
      if (iamin_LNDID) then
         call domain_areafactinit_mct(cdata_rr,mdl2drv_rr,drv2mdl_rr,'areafact_r')
         call mct_avect_vecmult(r2x_rr,mdl2drv_rr,seq_flds_r2x_fluxes)
      endif
      call map_rofr2rofx_mct(cdata_rr, r2x_rr, cdata_rx, r2x_rx)
   endif

   if (iamin_CPLLNDID .and. sno_present) then
      call map_snox2snos_mct( cdata_sx, dom_sx%data, cdata_ss, dom_ss%data)
      if (iamin_LNDID) then
         call domain_areafactinit_mct(cdata_ss,mdl2drv_ss,drv2mdl_ss,'areafact_s')
         call mct_avect_vecmult(s2x_ss,mdl2drv_ss,seq_flds_s2x_fluxes)
      endif
      call map_snos2snox_mct(cdata_ss, s2x_ss, cdata_sx, s2x_sx)
   endif

   if (iamin_CPLOCNID .and. ocn_present) then
      call map_ocnx2ocno_mct( cdata_ox, dom_ox%data, cdata_oo, dom_oo%data)
      if (iamin_OCNID) then
         call domain_areafactinit_mct(cdata_oo,mdl2drv_oo,drv2mdl_oo,'areafact_o')
         call mct_avect_vecmult(o2x_oo,mdl2drv_oo,seq_flds_o2x_fluxes)
      endif
      call map_ocno2ocnx_mct(cdata_oo, o2x_oo, cdata_ox, o2x_ox)
   endif

   if (iamin_CPLICEID .and. ice_present) then
      call map_icex2icei_mct( cdata_ix, dom_ix%data, cdata_ii, dom_ii%data)
      if (iamin_ICEID) then
         call domain_areafactinit_mct(cdata_ii,mdl2drv_ii,drv2mdl_ii,'areafact_i')
         call mct_avect_vecmult(i2x_ii,mdl2drv_ii,seq_flds_i2x_fluxes)
      endif
      call map_icei2icex_mct(cdata_ii, i2x_ii, cdata_ix, i2x_ix)
   endif

   if (iamin_CPLGLCID .and. glc_present) then
      call map_glcx2glcg_mct( cdata_gx, dom_gx%data, cdata_gg, dom_gg%data)
      if (iamin_GLCID) then
         call domain_areafactinit_mct(cdata_gg,mdl2drv_gg,drv2mdl_gg,'areafact_g')
         call mct_avect_vecmult(g2x_gg,mdl2drv_gg,seq_flds_g2x_fluxes)
      endif
      call map_glcg2glcx_mct(cdata_gg, g2x_gg, cdata_gx, g2x_gx)
   endif

   !-----------------------------------------------------------------------------
   ! global sum diagnostics for IC data
   !-----------------------------------------------------------------------------
   if (iamin_CPLID .and. info_debug > 1) then
      if (drv_threading) call seq_comm_setnthreads(nthreads_CPLID)
      if (atm_present) call seq_diag_avect_mct(cdata_ax,a2x_ax,'recv atm IC')
      if (ice_present) call seq_diag_avect_mct(cdata_ix,i2x_ix,'recv ice IC')
      if (lnd_present) call seq_diag_avect_mct(cdata_lx,l2x_lx,'recv lnd IC')
      if (rof_present) call seq_diag_avect_mct(cdata_rx,r2x_rx,'recv roff IC')
      if (sno_present) call seq_diag_avect_mct(cdata_sx,s2x_sx,'recv sno IC')
      if (ocn_present) call seq_diag_avect_mct(cdata_ox,o2x_ox,'recv ocn IC')
      if (glc_present) call seq_diag_avect_mct(cdata_gx,g2x_gx,'recv glc IC')
      if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
   end if

   !-----------------------------------------------------------------------------
   ! Initialize fractions
   !-----------------------------------------------------------------------------

   if (iamin_CPLID) then
      if (drv_threading) call seq_comm_setnthreads(nthreads_CPLID)
      if ( seq_comm_iamroot(CPLID)) write(logunit,F00) 'Initializing fractions'
      call seq_frac_init(cdata_ax, cdata_ix, cdata_lx, cdata_ox, cdata_gx, &
                         ice_present, ocn_present, lnd_present, glc_present, &
                         dead_comps, &
                         fractions_ax, fractions_ix, fractions_lx, fractions_ox, &
                         fractions_gx)
      if ( seq_comm_iamroot(CPLID)) write(logunit,F00) 'Setting fractions '
      call seq_frac_set(i2x_ix, &
                        cdata_ax, cdata_ix, cdata_lx, cdata_ox, cdata_gx, &
                        ice_present, ocn_present, lnd_present, glc_present, &
                        fractions_ax, fractions_ix, fractions_lx, fractions_ox, &
                        fractions_gx)

      !-----------------------------------------------------------------------------
      ! Initialize atm/ocn flux component and compute ocean albedos
      !-----------------------------------------------------------------------------
      if (ocn_present) then
         if ( seq_comm_iamroot(CPLID)) write(logunit,F00) 'Initializing atm/ocn flux component'
         ! note: albedo_only mode doesn't use a2x_ox or o2x_ox or a2x_ax or o2x_ax
         ! Initialize attribute vector
         call mct_aVect_init(xao_ox, rList=seq_flds_xao_fields, lsize=mct_aVect_lsize(o2x_ox))
         call mct_aVect_zero(xao_ox)
         if (trim(aoflux_grid) == 'ocn') then
            call seq_flux_init_mct(cdata_ox,fractions_ox)
         elseif (trim(aoflux_grid) == 'atm') then
            call seq_flux_init_mct(cdata_ax,fractions_ax)
         elseif (trim(aoflux_grid) == 'exch') then
            call seq_flux_initexch_mct(cdata_ax,cdata_ox)
         endif
         call seq_flux_ocnalb_mct(cdata_ox,xao_ox,fractions_ox)
      endif

      if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
   endif

   !-----------------------------------------------------------------------------
   ! Recalculate initial solar. Merge atmosphere input state and run atmospheric radiation
   ! tcx - for initialization only?
   !-----------------------------------------------------------------------------

   call t_startf('driver_init_atminit')

   if (atm_prognostic) then
      if (iamin_CPLID) then
         if (drv_threading) call seq_comm_setnthreads(nthreads_CPLID)
         if (lnd_present) then
            if ( seq_comm_iamroot(CPLID)) write(logunit,F00) 'Calling map_lnd2atm_mct'
            call map_lnd2atm_mct( cdata_lx, l2x_lx, cdata_ax, l2x_ax, &
                                  fractions_l=fractions_lx, fractions_a=fractions_ax, &
                                  fluxlist=seq_flds_l2x_fluxes, statelist=seq_flds_l2x_states )
         endif
         if (ocn_present) then
            if ( seq_comm_iamroot(CPLID)) write(logunit,F00) 'Calling map_ocn2atm_mct for mapping o2x_ox to o2x_ax'
            call map_ocn2atm_mct( cdata_ox, o2x_ox, cdata_ax, o2x_ax, &
                                  fractions_o=fractions_ox, fractions_a=fractions_ax, &
                                  statelist=seq_flds_o2x_states )
            call map_ocn2atm_mct( cdata_ox, o2x_ox, cdata_ax, o2x_ax, &
                                  fluxlist=seq_flds_o2x_fluxes )
            call map_ocn2atm_mct( cdata_ox, xao_ox, cdata_ax, xao_ax, &
                                  fractions_o=fractions_ox, fractions_a=fractions_ax, &
                                  statelist=seq_flds_xao_albedo )
            if (trim(aoflux_grid) == 'ocn') then
               if ( seq_comm_iamroot(CPLID)) &
                  write(logunit,F00) 'Calling map_ocn2atm_mct for mapping xao_ox to xao_ax'
               call map_ocn2atm_mct( cdata_ox, xao_ox, cdata_ax, xao_ax, &
                                     fractions_o=fractions_ox, fractions_a=fractions_ax, &
                                     fluxlist=seq_flds_xao_fluxes, statelist=seq_flds_xao_states ) 
            endif
            if (trim(aoflux_grid) == 'atm') then
               if ( seq_comm_iamroot(CPLID)) &
                  write(logunit,F00) 'Calling map_atm2ocn_mct for mapping xao_ax to xao_ox'
! tcraig: this mapping has to be done with area overlap mapping for all fields 
! due to the masking of the xao_ax data and the fact that states are mapped with 
! bilinear mapping currently
!               call map_atm2ocn_mct( cdata_ax, xao_ax, cdata_ox, xao_ox, &
!                                     fluxlist=seq_flds_xao_fluxes, statelist=seq_flds_xao_states )
               call map_atm2ocn_mct( cdata_ax, xao_ax, cdata_ox, xao_ox, &
                                     fluxlist=seq_flds_xao_states//":"//seq_flds_xao_fluxes)
            endif
         endif
         if (ice_present) then
            if ( seq_comm_iamroot(CPLID)) write(logunit,F00) 'Calling map_ice2atm_mct for mapping i2x_ix to i2x_ax'
            call map_ice2atm_mct( cdata_ix, i2x_ix, cdata_ax, i2x_ax, &
                                  fractions_i=fractions_ix, fractions_a=fractions_ax, &
                                  fluxlist=seq_flds_i2x_fluxes, statelist=seq_flds_i2x_states ) 
         endif
         if (lnd_present .or. ocn_present) then
            if ( seq_comm_iamroot(CPLID)) write(logunit,F00) 'Calling mrg_x2a_run_mct'
            call mrg_x2a_run_mct( cdata_ax, l2x_ax, o2x_ax, xao_ax, i2x_ax, fractions_ax, x2a_ax )
         endif
   
         if (info_debug > 1) call seq_diag_avect_mct(cdata_ax,x2a_ax,'send atm IC2')
         if ( seq_comm_iamroot(CPLID)) write(logunit,F00) 'Calling atm_init_mct'
   
         if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
      endif

      if (iamin_CPLATMID) then
         call map_atmx2atma_mct( cdata_ax, x2a_ax, cdata_aa, x2a_aa)
         call seq_infodata_exchange(infodata,CPLATMID,'cpl2atm_init')
      endif
   endif  ! atm_prognostic

   !-----------------------------------------------------------------------------
   ! Second phase of atmosphere component initialization, recalculate solar based 
   ! on input albedo's from surface components. Data or dead atmosphere may just
   ! return on this phase.
   !-----------------------------------------------------------------------------

   if (iamin_ATMID) then
      call t_adj_detailf(+2)
      if (drv_threading) call seq_comm_setnthreads(nthreads_ATMID)
      call seq_infodata_putData(infodata,atm_phase=2)
      call mct_avect_vecmult(x2a_aa,drv2mdl_aa,seq_flds_x2a_fluxes)
!wangty modify
#ifdef wrf
      call atm_init_mct( EClock_a, cdata_aa, cdata_cc, cdata_caca, x2a_aa, a2x_aa, &
                         x2c_cc1, x2c_cc2,  c2x_cc1, c2x_cc2, &
                         x2ca_caca1, x2ca_caca2,  ca2x_caca1, ca2x_caca2, &
                         twoway_coupling, twoway_nudging) !juanxiong he      
#else 
      call atm_init_mct( EClock_a, cdata_aa, x2a_aa, a2x_aa)
#endif
      call mct_avect_vecmult(a2x_aa,mdl2drv_aa,seq_flds_a2x_fluxes)
      if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
      call t_adj_detailf(-2)
   endif

   if (iamin_CPLATMID) then
      call map_atma2atmx_mct( cdata_aa, a2x_aa, cdata_ax, a2x_ax)
!wangty modify
#ifdef wrf
      call map_cama2camx_mct(cdata_cc, c2x_cc1, cdata_cx, c2x_cx1)  !juanxiong he
      call map_cama2camx_mct(cdata_cc, c2x_cc2, cdata_cx, c2x_cx2)  !juanxiong he
      call map_gcama2camx_mct(cdata_caca, ca2x_caca1, cdata_cax, ca2x_cax1) !juanxiong he
      call map_gcama2camx_mct(cdata_caca, ca2x_caca2, cdata_cax, ca2x_cax2) !juanxiong he
#endif
      call seq_infodata_exchange(infodata,CPLATMID,'atm2cpl_init') 
   endif

   if (iamin_CPLID) then
      if (drv_threading) call seq_comm_setnthreads(nthreads_CPLID)
      if (info_debug > 1) call seq_diag_avect_mct(cdata_ax,a2x_ax,'recv atm IC2')
      if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
   endif
!wangty modify
#ifdef wrf
   !------------------------------------------------------------------
   ! wrf  and geatm initial, second phase, juanxiong he
   !------------------------------------------------------------------

   if (iamin_CPLID) then
!            call seq_hist_write(EClock_d)
            call map_cam2wrf_mct( cdata_cx, c2x_cx1, cdata_mx, c2x_mx1 , &
                                    statelist=seq_flds_c2x_states ) ! juanxiong he
            call map_cam2wrf_mct( cdata_cx, c2x_cx2, cdata_mx, c2x_mx2 , &
                                    statelist=seq_flds_c2x_states ) ! juanxiong he
            call mrg_x2w_run_mct( cdata_mx, c2x_mx1, x2m_mx1)  ! juanxiong he
            call mrg_x2w_run_mct( cdata_mx, c2x_mx2, x2m_mx2)  ! juanxiong he
            call map_cam2gea_mct( cdata_cax, ca2x_cax1, cdata_gex, ca2x_chemx1 , &
                                  statelist=seq_flds_ca2x_states ) ! juanxiong he
            call map_cam2gea_mct( cdata_cax, ca2x_cax2, cdata_gex, ca2x_chemx2 , &
                                  statelist=seq_flds_ca2x_states ) ! juanxiong he
            call mrg_x2ge_run_mct( cdata_gex, ca2x_chemx1, x2chem_chemx1)  ! juanxiong he
            call mrg_x2ge_run_mct( cdata_gex, ca2x_chemx2, x2chem_chemx2)  ! juanxiong he
   endif

   if (iamin_CPLWRFID .and. wrf_prognostic) then
            call t_drvstartf ('driver_c2w_wrfx2wrfa',barrier=mpicom_CPLWRFID)
            call map_wrfx2wrfw_mct( cdata_mx, x2m_mx1, cdata_mm, x2m_mm1)   ! juaxniong he
            call map_wrfx2wrfw_mct( cdata_mx, x2m_mx2, cdata_mm, x2m_mm2)   ! juaxniong he
            call t_drvstopf  ('driver_c2w_wrfx2wrfa')
   endif

   if (iamin_WRFID) then
      call t_adj_detailf(+2)
      if (drv_threading) call seq_comm_setnthreads(nthreads_WRFID)
      call seq_infodata_putData(infodata,wrf_phase=2)
      call wrf_init_mct( EClock_w, cdata_ww, cdata_mm, x2w_ww, w2x_ww, x2m_mm1, x2m_mm2, m2x_mm, &
                         twoway_coupling, twoway_nudging )    ! juanxiong he
      if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
      twoway_coupling = .False.
      call t_adj_detailf(-2)
   endif

   if (iamin_CPLGEAID .and. geatm_prognostic) then
            call t_drvstartf ('driver_ca2ge_geax2geaa',barrier=mpicom_CPLGEAID)
            call map_geax2geaw_mct( cdata_gex, x2chem_chemx1, cdata_gege, x2chem_chemchem1)   !juaxniong he
            call map_geax2geaw_mct( cdata_gex, x2chem_chemx2, cdata_gege, x2chem_chemchem2)   !juaxniong he
            call t_drvstopf  ('driver_ca2ge_geax2geaa')
   endif

   if (iamin_GEAID) then
      call t_adj_detailf(+2)
      if (drv_threading) call seq_comm_setnthreads(nthreads_GEAID)
      call seq_infodata_putData(infodata,geatm_phase=2)
      call geatm_init_mct( EClock_ge, cdata_gege, & 
                           x2chem_chemchem1, x2chem_chemchem2, chem2x_chemchem ) ! juanxiong he
      if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
      call t_adj_detailf(-2)
   endif
#endif
   call t_stopf  ('driver_init_atminit')

   !-----------------------------------------------------------------------------
   ! Read driver restart file, overwrite anything previously sent or computed
   !-----------------------------------------------------------------------------

   call t_startf('driver_init_readrestart')
   call seq_diag_zero_mct(mode='all')
   if (read_restart) call seq_rest_read(rest_file)
   call t_stopf  ('driver_init_readrestart')

   if (do_histinit) then
      if (iamin_CPLID) then
         if (drv_threading) call seq_comm_setnthreads(nthreads_CPLID)
         if (iamroot_CPLID) then
            call seq_timemgr_EClockGetData( EClock_d, curr_ymd=ymd, curr_tod=tod )
            write(logunit,104) ' Write history file at ',ymd,tod
            call shr_sys_flush(logunit)
         endif
         call seq_hist_write(EClock_d)
         if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
      endif
   endif

   if ( iamroot_CPLID )then
      write(logunit,*) ' '
      write(logunit,F00) 'Model initialization complete '
      write(logunit,*) ' '
      call shr_sys_flush(logunit)
   endif

   call t_stopf  ('DRIVER_INIT')

end subroutine ccsm_init



!===============================================================================

subroutine ccsm_run()

 101  format( A, 2i8, 12A, A, F8.2, A, F8.2 )
 102  format( A, 2i8, A, 5L3 )
 103  format( 5A )
 104  format( A, 2i8)
 105  format( A, 2i8, A, f10.2, A, f10.2, A, A, i5, A, A)
 106  format( A, f23.12)

   call seq_infodata_putData(infodata,atm_phase=1,lnd_phase=1,ocn_phase=1,ice_phase=1)
   call seq_timemgr_EClockGetData( EClock_d, stepno=begstep)
   call seq_timemgr_EClockGetData( EClock_d, dtime=dtime)
   ncpl = 86400/dtime
   dtstep_acc = 0._r8
   dtstep_cnt = 0
   stop_alarm = seq_timemgr_alarmIsOn(EClock_d,seq_timemgr_alarm_stop)
   if (seq_timemgr_alarmIsOn(EClock_d,seq_timemgr_alarm_datestop)) then
      if (iamroot_CPLID) then
          write(logunit,*) ' '
          write(logunit,103) subname,' NOTE: Stopping from alarm STOP DATE'
          write(logunit,*) ' '
      endif
      stop_alarm = .true.
   endif

   !----------------------------------------------------------
   ! Beginning of basic time step loop
   !----------------------------------------------------------

   call t_startf ('DRIVER_RUN_LOOP_BSTART')
   call mpi_barrier(mpicom_GLOID,ierr)
   call t_stopf ('DRIVER_RUN_LOOP_BSTART')
   Time_begin = mpi_wtime()
   Time_bstep = mpi_wtime()
   do while ( .not. stop_alarm)

      call t_startf('DRIVER_RUN_LOOP')
      call t_drvstartf ('DRIVER_CLOCK_ADVANCE',cplrun=.true.)

      !----------------------------------------------------------
      ! Advance sync clock time (this is time that models should have before 
      ! they return to the driver).  Write timestamp and run alarm status
      !----------------------------------------------------------

      call seq_timemgr_clockAdvance( seq_SyncClock)
      call seq_timemgr_EClockGetData( EClock_d, curr_ymd=ymd, curr_tod=tod )
      call shr_cal_date2ymd(ymd,year,month,day)
      stop_alarm    = seq_timemgr_alarmIsOn(EClock_d,seq_timemgr_alarm_stop)
      atmrun_alarm  = seq_timemgr_alarmIsOn(EClock_d,seq_timemgr_alarm_atmrun)
!wangty modify
#ifdef wrf
      wrfrun_alarm  = seq_timemgr_alarmIsOn(EClock_d,seq_timemgr_alarm_wrfrun) !juanxiong he
      gearun_alarm  = seq_timemgr_alarmIsOn(EClock_d,seq_timemgr_alarm_gearun) !juanxiong he
#endif
      lndrun_alarm  = seq_timemgr_alarmIsOn(EClock_d,seq_timemgr_alarm_lndrun)
      icerun_alarm  = seq_timemgr_alarmIsOn(EClock_d,seq_timemgr_alarm_icerun)
      glcrun_alarm  = seq_timemgr_alarmIsOn(EClock_d,seq_timemgr_alarm_glcrun)
      ocnrun_alarm  = seq_timemgr_alarmIsOn(EClock_d,seq_timemgr_alarm_ocnrun)
      ocnnext_alarm = seq_timemgr_alarmIsOn(EClock_d,seq_timemgr_alarm_ocnnext)
      restart_alarm = seq_timemgr_alarmIsOn(EClock_d,seq_timemgr_alarm_restart)
      history_alarm = seq_timemgr_alarmIsOn(EClock_d,seq_timemgr_alarm_history)
      histavg_alarm = seq_timemgr_alarmIsOn(EClock_d,seq_timemgr_alarm_histavg)
      tprof_alarm   = seq_timemgr_alarmIsOn(EClock_d,seq_timemgr_alarm_tprof)

      ! this probably belongs in seq_timemgr somewhere using proper clocks
      t1hr_alarm = .false.
      t2hr_alarm = .false.
      t3hr_alarm = .false.
      t6hr_alarm = .false.
      t12hr_alarm = .false.
      t24hr_alarm = .false.
      if (mod(tod, 3600) == 0) t1hr_alarm = .true.
      if (mod(tod, 7200) == 0) t2hr_alarm = .true.
      if (mod(tod,10800) == 0) t3hr_alarm = .true.
      if (mod(tod,21600) == 0) t6hr_alarm = .true.
      if (mod(tod,43200) == 0) t12hr_alarm = .true.
      if (tod == 0) t24hr_alarm = .true.

      call seq_infodata_putData(infodata, glcrun_alarm=glcrun_alarm)

      if (seq_timemgr_alarmIsOn(EClock_d,seq_timemgr_alarm_datestop)) then
         if (iamroot_CPLID) then
             write(logunit,*) ' '
             write(logunit,103) subname,' NOTE: Stopping from alarm STOP DATE'
             write(logunit,*) ' '
         endif
         stop_alarm = .true.
      endif

      ! update the orbital data as needed
      if (trim(orb_mode) == trim(seq_infodata_orb_variable_year)) then
         orb_nyear =  orb_iyear + (year - orb_iyear_align)
         if (orb_nyear /= orb_cyear) then
            orb_cyear = orb_nyear
            call shr_orb_params(orb_cyear, orb_eccen, orb_obliq, orb_mvelp, &
                                orb_obliqr, orb_lambm0, orb_mvelpp, iamroot_CPLID)
            call seq_infodata_putData(infodata,orb_eccen=orb_eccen,orb_obliqr=orb_obliqr, &
                 orb_lambm0=orb_lambm0,orb_mvelpp=orb_mvelpp)
         endif
      endif

      ! override ocnrun_alarm and ocnnext_alarm for first ocn run
      ! skip_ocean_run is initialized above to true if it's a startup
      ! if it's not a startup, ignore all of this
      ! stop the overide on the second ocnrun_alarm

      if (ocnrun_alarm) ocnrun_count = ocnrun_count + 1
      if (ocnrun_count > 1) skip_ocean_run = .false.
      if (skip_ocean_run) then
         ocnrun_alarm = .false.
         ocnnext_alarm = .false.
      endif

      if (iamroot_CPLID) then
	     CALL PUSH_MODULEID(MODULE_CPL)
         if (loglevel > 1) then
!wangty modify
#ifdef wrf
            write(logunit,102) ' Alarm_state: model date = ',ymd,tod, &
               ' aliog run alarms = ',  atmrun_alarm, lndrun_alarm, &
                         icerun_alarm, ocnrun_alarm, glcrun_alarm, wrfrun_alarm, gearun_alarm !juanxiong he
#else
            write(logunit,102) ' Alarm_state: model date = ',ymd,tod, &
               ' aliog run alarms = ',  atmrun_alarm, lndrun_alarm, &
                         icerun_alarm, ocnrun_alarm, glcrun_alarm
#endif
            write(logunit,102) ' Alarm_state: model date = ',ymd,tod, &
               ' 1.2.3.6.12 run alarms = ',  t1hr_alarm, t2hr_alarm, &
                         t3hr_alarm, t6hr_alarm, t12hr_alarm, t24hr_alarm
            call shr_sys_flush(logunit)
         endif
		 CALL POP_MODULEID()
      endif

      call t_drvstopf  ('DRIVER_CLOCK_ADVANCE',cplrun=.true.)

      !----------------------------------------------------------
      ! OCN/ICE PREP
      ! Map for ice prep and atmocn flux
      !----------------------------------------------------------

      if (iamin_CPLID .and. (ice_present.or.ocn_present)) then
         CALL PUSH_MODULEID(MODULE_CPL)
		 call t_drvstartf ('DRIVER_OCNPREP',cplrun=.true.,barrier=mpicom_CPLID)
         if (drv_threading) call seq_comm_setnthreads(nthreads_CPLID)
         call t_drvstartf ('driver_ocnprep_atm2ocn',barrier=mpicom_CPLID)
         call map_atm2ocn_mct( cdata_ax, a2x_ax, cdata_ox, a2x_ox, &
                               fluxlist=seq_flds_a2x_fluxes, statelist=seq_flds_a2x_states )
         call t_drvstopf  ('driver_ocnprep_atm2ocn')
         if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
         call t_drvstopf  ('DRIVER_OCNPREP',cplrun=.true.)
         CALL POP_MODULEID()
	  endif

      !----------------------------------------------------------
      ! OCN SETUP
      !----------------------------------------------------------

      if (ocn_present .and. ocnrun_alarm) then
          
         !----------------------------------------------------
         ! "startup" wait
         !----------------------------------------------------

         if (iamin_CPLOCNID .and. cpl2ocn_first) then
            CALL PUSH_MODULEID(MODULE_CPLOCN)
			! want to know the time the ocean pes waited for the cpl pes
            !   at the first ocnrun_alarm, min ocean wait is wait time
            ! do not use t_barrierf here since it can be "off", use mpi_barrier
            if (iamin_OCNID) then
				CALL PUSH_MODULEID(MODULE_OCN)
				call t_drvstartf ('DRIVER_C2O_INITWAIT')
				CALL POP_MODULEID()
			endif
			call mpi_barrier(mpicom_CPLOCNID,ierr)
            if (iamin_OCNID) then
				CALL PUSH_MODULEID(MODULE_OCN)
				call t_drvstopf  ('DRIVER_C2O_INITWAIT')
				CALL POP_MODULEID()
			endif
			cpl2ocn_first = .false.
            CALL POP_MODULEID()
		 endif

         !----------------------------------------------------
         ! ocn prep
         !----------------------------------------------------

         if (iamin_CPLID .and. ocn_prognostic) then
            CALL PUSH_MODULEID(MODULE_CPL)
			call t_drvstartf ('DRIVER_OCNPREP',cplrun=.true.,barrier=mpicom_CPLID)
            if (drv_threading) call seq_comm_setnthreads(nthreads_CPLID)
            call t_drvstartf ('driver_ocnprep_avg',barrier=mpicom_CPLID)
            ! temporary formation of average
!           call mct_accum_average(x2oacc_ox)
            if (x2oacc_ox_cnt > 0) then
               x2oacc_ox%data%rAttr = x2oacc_ox%data%rAttr / (x2oacc_ox_cnt*1.0_r8)
            endif
            x2oacc_ox_cnt = 0
            call t_drvstopf  ('driver_ocnprep_avg')
            if (rof_present .and. ocnrof_prognostic) then
               ! Map runoff to ocn, average, put in x2oacc_ox
               if (r2xacc_rx_cnt > 0) then
                  call t_drvstartf ('driver_ocnprep_ravg',barrier=mpicom_CPLID)
                  r2xacc_rx%data%rAttr = r2xacc_rx%data%rAttr / (r2xacc_rx_cnt*1.0_r8)
                  r2xacc_rx_cnt = 0
                  call t_drvstopf ('driver_ocnprep_ravg')
                  call t_drvstartf ('driver_ocnprep_rof2ocn',barrier=mpicom_CPLID)
                  call map_rof2ocn_mct( cdata_rx, r2xacc_rx%data, cdata_ox, r2x_ox ) 
                  if (do_hist_r2x) then
                     call seq_hist_writeaux(EClock_d,'r2xacc','domr',cdata_rx,r2xacc_rx%data, &
                          rof_nx,rof_ny,1)
                  endif
                  call t_drvstopf  ('driver_ocnprep_rof2ocn')
                  call t_drvstartf ('driver_ocnprep_rofcopy',barrier=mpicom_CPLID)
                  call mct_aVect_copy(aVin=r2x_ox, aVout=x2oacc_ox%data)
                  call t_drvstopf  ('driver_ocnprep_rofcopy')
               endif
            endif
            if (info_debug > 1) then
               call t_drvstartf ('driver_ocnprep_diagav',barrier=mpicom_CPLID)
               call seq_diag_avect_mct(cdata_ox,x2oacc_ox%data,'send ocn')
               call t_drvstopf  ('driver_ocnprep_diagav')
            endif
            if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
            call t_drvstopf  ('DRIVER_OCNPREP',cplrun=.true.)
            CALL POP_MODULEID()
		 endif

         !----------------------------------------------------
         ! cpl -> ocn
         !----------------------------------------------------

         if (iamin_CPLOCNID .and. ocn_prognostic) then
            CALL PUSH_MODULEID(MODULE_CPLOCN)
			call t_drvstartf ('DRIVER_C2O',barrier=mpicom_CPLOCNID)
            call t_drvstartf ('driver_c2o_ocnx2ocno',barrier=mpicom_CPLOCNID)
            call map_ocnx2ocno_mct( cdata_ox, x2oacc_ox%data, cdata_oo, x2o_oo)
            call t_drvstopf  ('driver_c2o_ocnx2ocno')
            call t_drvstartf ('driver_c2o_infoexch',barrier=mpicom_CPLOCNID)
            call seq_infodata_exchange(infodata,CPLOCNID,'cpl2ocn_run')
            call t_drvstopf  ('driver_c2o_infoexch')
            call t_drvstopf  ('DRIVER_C2O')
            CALL POP_MODULEID()
		 endif

      endif
  
      !----------------------------------------------------------
      ! LND SETUP
      !----------------------------------------------------------

      if (lnd_present .and. lndrun_alarm) then

         !----------------------------------------------------
         ! lnd prep
         !----------------------------------------------------

         if (iamin_CPLID) then
		    CALL PUSH_MODULEID(MODULE_CPL)
            call t_drvstartf ('DRIVER_LNDPREP',cplrun=.true.,barrier=mpicom_CPLID)
            if (drv_threading) call seq_comm_setnthreads(nthreads_CPLID)

            if (lnd_prognostic) then
               call t_drvstartf ('driver_lndprep_atm2lnd',barrier=mpicom_CPLID)
               call map_atm2lnd_mct( cdata_ax, a2x_ax, cdata_lx, a2x_lx )
               call t_drvstopf  ('driver_lndprep_atm2lnd')
               call t_drvstartf ('driver_lndprep_mrgx2l',barrier=mpicom_CPLID)
               call mrg_x2l_run_mct( cdata_lx, a2x_lx, x2l_lx )
               call t_drvstopf  ('driver_lndprep_mrgx2l')
               if (info_debug > 1) then
                  call t_drvstartf ('driver_lndprep_diagav',barrier=mpicom_CPLID)
                  call seq_diag_avect_mct(cdata_lx,x2l_lx,'send lnd')
                  call t_drvstopf  ('driver_lndprep_diagav')
               endif
            endif

            if (glc_present .and. sno_prognostic) then
               if (info_debug > 1) then
                  call t_drvstartf ('driver_lndprep_diagav',barrier=mpicom_CPLID)
                  call seq_diag_avect_mct(cdata_sx,x2s_sx,'send sno')
                  call t_drvstopf  ('driver_lndprep_diagav')
               endif
            endif

            if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
            call t_drvstopf  ('DRIVER_LNDPREP',cplrun=.true.)
            CALL POP_MODULEID()
		 endif

         !----------------------------------------------------
         ! cpl -> lnd
         !----------------------------------------------------

         if (iamin_CPLLNDID) then
		    CALL PUSH_MODULEID(MODULE_CPLLND)
            call t_drvstartf ('DRIVER_C2L',barrier=mpicom_CPLLNDID)
            if (lnd_prognostic) then
               call t_drvstartf ('driver_c2l_lndx2lndl',barrier=mpicom_CPLLNDID)
               call map_lndx2lndl_mct( cdata_lx, x2l_lx, cdata_ll, x2l_ll)
               call t_drvstopf  ('driver_c2l_lndx2lndl')
            endif
            if (glc_present .and. sno_prognostic) then
               call t_drvstartf ('driver_c2l_snox2snos',barrier=mpicom_CPLLNDID)
               call map_snox2snos_mct( cdata_sx, x2s_sx, cdata_ss, x2s_ss)
               call t_drvstopf  ('driver_c2l_snox2snos')
            endif
            if (lnd_prognostic .or. sno_prognostic) then
               call t_drvstartf ('driver_c2l_infoexch',barrier=mpicom_CPLLNDID)
               call seq_infodata_exchange(infodata,CPLLNDID,'cpl2lnd_run')
               call t_drvstopf  ('driver_c2l_infoexch')
            endif
            call t_drvstopf  ('DRIVER_C2L')
            CALL POP_MODULEID()
		 endif

      endif

      !----------------------------------------------------------
      ! ICE SETUP
      ! Note that for atm->ice mapping below will leverage the assumption that the
      ! ice and ocn are on the same grid and that mapping of atm to ocean is 
      ! done already for use by atmocn flux and ice model prep
      !----------------------------------------------------------

      if (ice_present .and. icerun_alarm) then

         !----------------------------------------------------
         ! ice prep
         !----------------------------------------------------

         if (iamin_CPLID .and. ice_prognostic) then
            CALL PUSH_MODULEID(MODULE_CPL)
			call t_drvstartf ('DRIVER_ICEPREP',cplrun=.true.,barrier=mpicom_CPLID)
            if (drv_threading) call seq_comm_setnthreads(nthreads_CPLID)
            call t_drvstartf ('driver_iceprep_ocn2ice',barrier=mpicom_CPLID)
            call map_ocn2ice_mct( cdata_ox, o2x_ox, cdata_ix, o2x_ix )
            call t_drvstopf  ('driver_iceprep_ocn2ice')
            
            call t_drvstartf ('driver_iceprep_atm2ice',barrier=mpicom_CPLID)
            call map_ocn2ice_mct( cdata_ox, a2x_ox, cdata_ix, a2x_ix )
!tcx fails            call map_atm2ice_mct( cdata_ax, a2x_ax, cdata_ix, a2x_ix )
            call t_drvstopf  ('driver_iceprep_atm2ice')
            
            call t_drvstartf ('driver_iceprep_mrgx2i',barrier=mpicom_CPLID)
            call mrg_x2i_run_mct( cdata_ix, a2x_ix, o2x_ix, x2i_ix )
            call t_drvstopf  ('driver_iceprep_mrgx2i')

            if (info_debug > 1) then
               call t_drvstartf ('driver_iceprep_diagav',barrier=mpicom_CPLID)
               call seq_diag_avect_mct(cdata_ix,x2i_ix,'send ice')
               call t_drvstopf  ('driver_iceprep_diagav')
            endif
            if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
            call t_drvstopf  ('DRIVER_ICEPREP',cplrun=.true.)
            CALL POP_MODULEID()
		 endif

         !----------------------------------------------------
         ! cpl -> ice
         !----------------------------------------------------

         if (iamin_CPLICEID .and. ice_prognostic) then
            CALL PUSH_MODULEID(MODULE_CPLICE)
			call t_drvstartf ('DRIVER_C2I',barrier=mpicom_CPLICEID)
            call t_drvstartf ('driver_c2i_icex2icei',barrier=mpicom_CPLICEID)
            call map_icex2icei_mct( cdata_ix, x2i_ix, cdata_ii, x2i_ii)
            call t_drvstopf  ('driver_c2i_icex2icei')
            call t_drvstartf ('driver_c2i_infoexch',barrier=mpicom_CPLICEID)
            call seq_infodata_exchange(infodata,CPLICEID,'cpl2ice_run')
            call t_drvstopf  ('driver_c2i_infoexch')
            call t_drvstopf  ('DRIVER_C2I')
            CALL POP_MODULEID()
		 endif

      endif

      !----------------------------------------------------------
      ! Run Ocn Model
      !----------------------------------------------------------

      if (ocn_present .and. ocnrun_alarm .and. iamin_OCNID) then
         CALL PUSH_MODULEID(MODULE_OCN)
		 if (run_barriers) then
            call t_drvstartf ('DRIVER_OCN_RUN_BARRIER')
            call mpi_barrier(mpicom_OCNID,ierr)
            call t_drvstopf ('DRIVER_OCN_RUN_BARRIER')
         endif
         call t_drvstartf ('DRIVER_OCN_RUN',barrier=mpicom_OCNID)
         if (drv_threading) call seq_comm_setnthreads(nthreads_OCNID)
         if (ocn_prognostic) call mct_avect_vecmult(x2o_oo,drv2mdl_oo,seq_flds_x2o_fluxes)
         call ocn_run_mct( EClock_o, cdata_oo, x2o_oo, o2x_oo)
         call mct_avect_vecmult(o2x_oo,mdl2drv_oo,seq_flds_o2x_fluxes)
         if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)         
         call t_drvstopf  ('DRIVER_OCN_RUN')
         CALL POP_MODULEID()
	  endif
 
      !----------------------------------------------------------
      ! Run Ice Model
      !----------------------------------------------------------

      if (ice_present .and. icerun_alarm .and. iamin_ICEID) then
         CALL PUSH_MODULEID(MODULE_ICE)
		 if (run_barriers) then
            call t_drvstartf ('DRIVER_ICE_RUN_BARRIER')
            call mpi_barrier(mpicom_ICEID,ierr)
            call t_drvstopf ('DRIVER_ICE_RUN_BARRIER')
         endif
         call t_drvstartf ('DRIVER_ICE_RUN',barrier=mpicom_ICEID)
         if (drv_threading) call seq_comm_setnthreads(nthreads_ICEID)
         if (ice_prognostic) call mct_avect_vecmult(x2i_ii,drv2mdl_ii,seq_flds_x2i_fluxes)
         call ice_run_mct( EClock_i, cdata_ii, x2i_ii, i2x_ii)
         call mct_avect_vecmult(i2x_ii,mdl2drv_ii,seq_flds_i2x_fluxes)
         if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
         call t_drvstopf  ('DRIVER_ICE_RUN')
         CALL POP_MODULEID()
	  endif

      !----------------------------------------------------------
      ! Run Land Model
      !----------------------------------------------------------

      if ((lnd_present.or.rof_present.or.sno_present) .and. & 
		lndrun_alarm .and. iamin_LNDID) then
         CALL PUSH_MODULEID(MODULE_LND)
		 if (run_barriers) then
            call t_drvstartf ('DRIVER_LND_RUN_BARRIER')
            call mpi_barrier(mpicom_LNDID,ierr)
            call t_drvstopf ('DRIVER_LND_RUN_BARRIER')
         endif
         call t_drvstartf ('DRIVER_LND_RUN',barrier=mpicom_LNDID)
         if (drv_threading) call seq_comm_setnthreads(nthreads_LNDID)
         if (lnd_prognostic) then
            call mct_avect_vecmult(x2l_ll,drv2mdl_ll,seq_flds_x2l_fluxes)
         endif
         if (sno_prognostic) then
            call mct_avect_vecmult(x2s_ss,drv2mdl_ss,seq_flds_x2s_fluxes)
         endif
         call lnd_run_mct( EClock_l, cdata_ll, x2l_ll, l2x_ll, &
                                     cdata_rr,         r2x_rr, &
                                     cdata_ss, x2s_ss, s2x_ss)
         call mct_avect_vecmult(l2x_ll,mdl2drv_ll,seq_flds_l2x_fluxes)
         if (rof_present) then
            call mct_avect_vecmult(r2x_rr,mdl2drv_rr,seq_flds_r2x_fluxes)
         endif
         if (sno_present) then
            call mct_avect_vecmult(s2x_ss,mdl2drv_ss,seq_flds_s2x_fluxes)
         endif
         if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
         call t_drvstopf  ('DRIVER_LND_RUN')
         CALL POP_MODULEID()
	  endif

      !----------------------------------------------------------
      ! ocn -> cpl, tight coupling (sequential type mode)
      !----------------------------------------------------------

      if (ocean_tight_coupling) then
      if (ocn_present .and. ocnnext_alarm) then
         if (iamin_CPLOCNID) then
		    CALL PUSH_MODULEID(MODULE_CPLOCN)
            call t_drvstartf ('DRIVER_O2C',barrier=mpicom_CPLOCNID)
            call t_drvstartf ('driver_o2c_ocno2ocnx',barrier=mpicom_CPLOCNID)
            call map_ocno2ocnx_mct( cdata_oo, o2x_oo, cdata_ox, o2x_ox)
            call t_drvstopf  ('driver_o2c_ocno2ocnx')
            call t_drvstartf ('driver_o2c_infoexch',barrier=mpicom_CPLOCNID)
            call seq_infodata_exchange(infodata,CPLOCNID,'ocn2cpl_run')
            call t_drvstopf  ('driver_o2c_infoexch')
            call t_drvstopf  ('DRIVER_O2C')
            CALL POP_MODULEID()
		 endif
         if (iamin_CPLID) then
            CALL PUSH_MODULEID(MODULE_CPL)
			call t_drvstartf  ('DRIVER_OCNPOST',cplrun=.true.,barrier=mpicom_CPLID)
            if (drv_threading) call seq_comm_setnthreads(nthreads_CPLID)
            if (info_debug > 1) then
               call t_drvstartf ('driver_ocnpost_diagav',barrier=mpicom_CPLID)
               call seq_diag_avect_mct(cdata_ox,o2x_ox,'recv ocn')
               call t_drvstopf  ('driver_ocnpost_diagav')
            endif
            if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
            call t_drvstopf  ('DRIVER_OCNPOST',cplrun=.true.)
            CALL POP_MODULEID()
		 endif
      endif
      endif

      !----------------------------------------------------------
      ! OCN PREP
      !----------------------------------------------------------

      if (ocn_present .and. iamin_CPLID) then
	     CALL PUSH_MODULEID(MODULE_CPL)
         call t_drvstartf ('DRIVER_ATMOCNP',cplrun=.true.,barrier=mpicom_CPLID)
         if (drv_threading) call seq_comm_setnthreads(nthreads_CPLID)
         if (ocn_prognostic) then

            ! Map ice to ocn
            if (ice_present) then
               call t_drvstartf ('driver_atmocnp_ice2ocn',barrier=mpicom_CPLID)
               call map_ice2ocn_mct( cdata_ix, i2x_ix, cdata_ox, i2x_ox)
               call t_drvstopf  ('driver_atmocnp_ice2ocn')
            endif

            ! Merge ocn inputs
            call t_drvstartf ('driver_atmocnp_mrgx2o',barrier=mpicom_CPLID)
            call mrg_x2o_run_mct( cdata_ox, a2x_ox, i2x_ox, xao_ox, fractions_ox, x2o_ox )
            call t_drvstopf  ('driver_atmocnp_mrgx2o')

            ! Accumulate ocn inputs
            ! Form partial sum of tavg ocn inputs (virtual "send" to ocn) 
            call t_drvstartf ('driver_atmocnp_accum',barrier=mpicom_CPLID)
!     !         call mct_accum_accumulate(x2o_ox, x2oacc_ox)
            if (x2oacc_ox_cnt == 0) then
               x2oacc_ox%data%rAttr = x2o_ox%rAttr
            else
               x2oacc_ox%data%rAttr = x2oacc_ox%data%rAttr + x2o_ox%rAttr
            endif
            x2oacc_ox_cnt = x2oacc_ox_cnt + 1
            call t_drvstopf  ('driver_atmocnp_accum')
         endif
 
         ! Compute atm/ocn fluxes (virtual "recv" from ocn)
         call t_drvstartf ('driver_atmocnp_flux',barrier=mpicom_CPLID)
         if (trim(aoflux_grid) == 'ocn') then
            call seq_flux_atmocn_mct( cdata_ox, a2x_ox, o2x_ox, xao_ox)
            call seq_flux_ocnalb_mct(cdata_ox,xao_ox,fractions_ox)
         else if (trim(aoflux_grid) == 'atm') then
            call seq_flux_atmocn_mct( cdata_ax, a2x_ax, o2x_ax, xao_ax)
            call seq_flux_ocnalb_mct(cdata_ox,xao_ox,fractions_ox)
         else if (trim(aoflux_grid) == 'exch') then
            call seq_flux_atmocnexch_mct( cdata_ax, cdata_ox, a2x_ax, o2x_ox, xao_ax, xao_ox, &
                                       fractions_ax, fractions_ox)
            call seq_flux_ocnalb_mct(cdata_ox,xao_ox,fractions_ox)
         endif  ! aoflux_grid
         call t_drvstopf  ('driver_atmocnp_flux')
         
         if (trim(aoflux_grid) == 'atm') then
            call t_drvstartf ('driver_atmocnp_atm2ocn',barrier=mpicom_CPLID)
! this mapping has to be done with area overlap mapping for all fields 
! due to the masking of the xao_ax data and the fact that a2oS is bilinear
!            call map_atm2ocn_mct( cdata_ax, xao_ax, cdata_ox, xao_ox, &
!                                  fluxlist=seq_flds_xao_fluxes, statelist=seq_flds_xao_states)
            call map_atm2ocn_mct( cdata_ax, xao_ax, cdata_ox, xao_ox, &
                                   fluxlist=seq_flds_xao_states//":"//seq_flds_xao_fluxes)
            call t_drvstopf  ('driver_atmocnp_atm2ocn')
         endif

         if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
         call t_drvstopf  ('DRIVER_ATMOCNP',cplrun=.true.)
         CALL POP_MODULEID()
	  endif

      !----------------------------------------------------------
      ! lnd -> cpl
      !----------------------------------------------------------

      if ((lnd_present.or.rof_present.or.sno_present) .and. lndrun_alarm) then

         if (iamin_CPLLNDID) then
		    CALL PUSH_MODULEID(MODULE_CPLLND)
            call t_drvstartf ('DRIVER_L2C',barrier=mpicom_CPLLNDID)
            if (lnd_present) then
               call t_drvstartf ('driver_l2c_lndl2lndx',barrier=mpicom_CPLLNDID)
               call map_lndl2lndx_mct( cdata_ll, l2x_ll, cdata_lx, l2x_lx)
               call t_drvstopf  ('driver_l2c_lndl2lndx')
            endif
            if (rof_present) then
               call t_drvstartf ('driver_l2c_rofr2rofx',barrier=mpicom_CPLLNDID)
               call map_rofr2rofx_mct( cdata_rr, r2x_rr, cdata_rx, r2x_rx)
               call t_drvstopf  ('driver_l2c_rofr2rofx')
            endif
            if (sno_present .and. glc_prognostic .and. glcrun_alarm) then
               call t_drvstartf ('driver_l2c_snos2snox',barrier=mpicom_CPLLNDID)
               call map_snos2snox_mct( cdata_ss, s2x_ss, cdata_sx, s2x_sx)
               call t_drvstopf  ('driver_l2c_snos2snox')
            endif
            call t_drvstartf ('driver_l2c_infoexch',barrier=mpicom_CPLLNDID)
            call seq_infodata_exchange(infodata,CPLLNDID,'lnd2cpl_run')
            call t_drvstopf  ('driver_l2c_infoexch')
            call t_drvstopf  ('DRIVER_L2C')
            CALL POP_MODULEID()
		 endif

         if (iamin_CPLID) then
		    CALL PUSH_MODULEID(MODULE_CPL)
            call t_drvstartf  ('DRIVER_LNDPOST',cplrun=.true.,barrier=mpicom_CPLID)
            if (drv_threading) call seq_comm_setnthreads(nthreads_CPLID)
            if (info_debug > 1) then
               call t_drvstartf ('driver_lndpost_diagav',barrier=mpicom_CPLID)
               if (lnd_present) then
                  call seq_diag_avect_mct(cdata_lx,l2x_lx,'recv lnd')
               endif
               if (rof_present) then
                  call seq_diag_avect_mct(cdata_rx,r2x_rx,'recv roff')
               endif
               if (sno_present .and. glc_prognostic .and. glcrun_alarm) then
                  call seq_diag_avect_mct(cdata_sx,s2x_sx,'recv sno')
               endif
               call t_drvstopf  ('driver_lndpost_diagav')
            endif
            if (rof_present .and. ocnrof_prognostic) then
               call t_drvstartf ('driver_lndpost_raccum',barrier=mpicom_CPLID)
               ! better to flux correct here if flux_epbalfact varies
               ! over the accumulation period
               call seq_infodata_GetData(infodata, flux_epbalfact = flux_epbalfact)
               if (r2xacc_rx_cnt == 0) then
                  r2xacc_rx%data%rAttr = r2x_rx%rAttr * flux_epbalfact
               else
                  r2xacc_rx%data%rAttr = r2xacc_rx%data%rAttr + r2x_rx%rAttr * flux_epbalfact
               endif
               r2xacc_rx_cnt = r2xacc_rx_cnt + 1
               call t_drvstopf ('driver_lndpost_raccum')
            endif
            if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
            call t_drvstopf  ('DRIVER_LNDPOST',cplrun=.true.)
            CALL POP_MODULEID()
		 endif

      endif   ! run alarm, lnd_present

      !----------------------------------------------------------
      ! GLC SETUP
      !----------------------------------------------------------

      if (sno_present .and. glcrun_alarm) then
         if (iamin_CPLID .and. glc_prognostic) then
		    CALL PUSH_MODULEID(MODULE_CPL)
            call t_drvstartf ('DRIVER_GLCPREP',cplrun=.true.,barrier=mpicom_CPLID)
            if (drv_threading) call seq_comm_setnthreads(nthreads_CPLID)

            ! Map sno to glc
            call t_drvstartf ('driver_glcprep_sno2glc',barrier=mpicom_CPLID)
            call map_sno2glc_mct( cdata_sx, s2x_sx, cdata_gx, s2x_gx ) 
            call t_drvstopf  ('driver_glcprep_sno2glc')

            ! Merge glc inputs
            call t_drvstartf ('driver_glcprep_mrgx2g',barrier=mpicom_CPLID)
            call mrg_x2g_run_mct( cdata_gx, s2x_gx, x2g_gx)
            call t_drvstopf  ('driver_glcprep_mrgx2g')

            if (info_debug > 1) then
               call t_drvstartf ('driver_glcprep_diagav',barrier=mpicom_CPLID)
               call seq_diag_avect_mct(cdata_gx,x2g_gx,'send glc')
               call t_drvstopf  ('driver_glcprep_diagav')
            endif

            if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
            call t_drvstopf  ('DRIVER_GLCPREP',cplrun=.true.)
            CALL POP_MODULEID()
		 endif

         !----------------------------------------------------
         ! cpl -> glc
         !----------------------------------------------------

         if (iamin_CPLGLCID .and. glc_prognostic) then
            CALL PUSH_MODULEID(MODULE_CPLGLC)
			call t_drvstartf ('DRIVER_C2G',barrier=mpicom_CPLGLCID)
            call t_drvstartf ('driver_c2g_glcx2glcg',barrier=mpicom_CPLGLCID)
            call map_glcx2glcg_mct( cdata_gx, x2g_gx, cdata_gg, x2g_gg)
            call t_drvstopf  ('driver_c2g_glcx2glcg')
            call t_drvstartf ('driver_c2g_infoexch',barrier=mpicom_CPLGLCID)
            call seq_infodata_exchange(infodata,CPLGLCID,'cpl2glc_run')
            call t_drvstopf  ('driver_c2g_infoexch')
            call t_drvstopf  ('DRIVER_C2G')
            CALL POP_MODULEID()
		 endif
      endif

      !----------------------------------------------------------
      ! budget with old fractions
      !----------------------------------------------------------

#if (defined NEW_BUDGET)
      if (iamin_CPLID .and. do_budgets) then
	     CALL PUSH_MODULEID(MODULE_CPL)
         call t_drvstartf ('DRIVER_BUDGET1',cplrun=.true.,budget=.true.,barrier=mpicom_CPLID)
         if (lnd_present) then
            call seq_diag_lnd_mct(dom_lx, fractions_lx, l2x_l=l2x_lx, x2l_l=x2l_lx)
         endif
         if (rof_present) then
            call seq_diag_rtm_mct(dom_rx, r2x_r=r2x_rx)
         endif
         if (ocn_present) then
         !  call seq_diag_ocn_mct(dom_ox, fractions_ox, o2x_o=o2x_ox, x2o_o=x2o_ox, xao_o=xao_ox)
            call seq_diag_ocn_mct(dom_ox, fractions_ox, o2x_o=o2x_ox, x2o_o=x2o_ox, xao_o=xao_ox, r2x_o=r2x_ox)
         endif
         if (ice_present) then
            call seq_diag_ice_mct(dom_ix, fractions_ix, x2i_i=x2i_ix)
         endif
         call t_drvstopf  ('DRIVER_BUDGET1',cplrun=.true.,budget=.true.)
         CALL POP_MODULEID()
	  endif
#endif

      !----------------------------------------------------------
      ! ice -> cpl
      !----------------------------------------------------------

      if (ice_present .and. icerun_alarm) then
         if (iamin_CPLICEID) then
		    CALL PUSH_MODULEID(MODULE_CPLICE)
            call t_drvstartf ('DRIVER_I2C',barrier=mpicom_CPLICEID)
            call t_drvstartf ('driver_i2c_icei2icex',barrier=mpicom_CPLICEID)
            call map_icei2icex_mct( cdata_ii, i2x_ii, cdata_ix, i2x_ix)
            call t_drvstopf  ('driver_i2c_icei2icex')
            call t_drvstartf ('driver_i2c_infoexch',barrier=mpicom_CPLICEID)
            call seq_infodata_exchange(infodata,CPLICEID,'ice2cpl_run')
            call t_drvstopf  ('driver_i2c_infoexch')
            call t_drvstopf  ('DRIVER_I2C')
            CALL POP_MODULEID()
		 endif

         if (iamin_CPLID) then
		    CALL PUSH_MODULEID(MODULE_CPL)
            call t_drvstartf  ('DRIVER_ICEPOST',cplrun=.true.,barrier=mpicom_CPLID)
            if (drv_threading) call seq_comm_setnthreads(nthreads_CPLID)
            if (info_debug > 1) then
               call t_drvstartf ('driver_icepost_diagav',barrier=mpicom_CPLID)
               call seq_diag_avect_mct(cdata_ix,i2x_ix,'recv ice')
               call t_drvstopf  ('driver_icepost_diagav')
            endif
            if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
            call t_drvstopf  ('DRIVER_ICEPOST',cplrun=.true.)
            CALL POP_MODULEID()
		 endif

      endif   ! run alarm, ice_present

      !----------------------------------------------------------
      ! Update fractions based on new ice fractions
      !----------------------------------------------------------

      if (iamin_CPLID) then
	     CALL PUSH_MODULEID(MODULE_CPL)
         call t_drvstartf ('DRIVER_FRACSET',cplrun=.true.,barrier=mpicom_CPLID)
         if (drv_threading) call seq_comm_setnthreads(nthreads_CPLID)
         call t_drvstartf ('driver_fracset_fracset',barrier=mpicom_CPLID)
         call seq_frac_set(i2x_ix, &
                           cdata_ax, cdata_ix, cdata_lx, cdata_ox, cdata_gx, &
                           ice_present, ocn_present, lnd_present, glc_present,  &
                           fractions_ax, fractions_ix, fractions_lx, fractions_ox, &
                           fractions_gx)
         call t_drvstopf  ('driver_fracset_fracset')
         if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
         call t_drvstopf  ('DRIVER_FRACSET',cplrun=.true.)
         CALL POP_MODULEID()
	  endif

      !----------------------------------------------------------
      ! ATM SETUP
      !----------------------------------------------------------

      if (atm_present .and. atmrun_alarm) then
 
         !----------------------------------------------------------
         ! atm prep
         !----------------------------------------------------------

         if (iamin_CPLID) then
		 CALL PUSH_MODULEID(MODULE_CPL)
         if (drv_threading) call seq_comm_setnthreads(nthreads_CPLID)
         call t_drvstartf ('DRIVER_ATMPREP',cplrun=.true.,barrier=mpicom_CPLID)
         if (atm_prognostic) then
            if (ocn_present) then
               if (trim(aoflux_grid) == 'ocn') then
                  call t_drvstartf ('driver_atmprep_ocn2atm2',barrier=mpicom_CPLID)
                  call map_ocn2atm_mct( cdata_ox, xao_ox, cdata_ax, xao_ax, &
                                        fractions_o=fractions_ox, fractions_a=fractions_ax, &
                                        fluxlist=seq_flds_xao_fluxes, statelist=seq_flds_xao_states )
                  call t_drvstopf  ('driver_atmprep_ocn2atm2')
               endif
            endif
            if (ocn_present) then
               call t_drvstartf ('driver_atmprep_ocn2atm1',barrier=mpicom_CPLID)
               call map_ocn2atm_mct( cdata_ox, o2x_ox, cdata_ax, o2x_ax, &
                                     fractions_o=fractions_ox, fractions_a=fractions_ax, &
                                     statelist=seq_flds_o2x_states )
               call map_ocn2atm_mct( cdata_ox, o2x_ox, cdata_ax, o2x_ax, &
                                     fluxlist=seq_flds_o2x_fluxes )
               call map_ocn2atm_mct( cdata_ox, xao_ox, cdata_ax, xao_ax, &
                                     fractions_o=fractions_ox, fractions_a=fractions_ax, &
                                     statelist=seq_flds_xao_albedo )
               call t_drvstopf  ('driver_atmprep_ocn2atm1')
            endif
            if (ice_present) then
               call t_drvstartf ('driver_atmprep_ice2atm',barrier=mpicom_CPLID)
               call map_ice2atm_mct( cdata_ix, i2x_ix, cdata_ax, i2x_ax, &
                                     fractions_i=fractions_ix, fractions_a=fractions_ax, &
                                     fluxlist=seq_flds_i2x_fluxes, statelist=seq_flds_i2x_states )
               call t_drvstopf  ('driver_atmprep_ice2atm')
            endif
            if (lnd_present) then
               call t_drvstartf ('driver_atmprep_lnd2atm',barrier=mpicom_CPLID)
               call map_lnd2atm_mct( cdata_lx, l2x_lx, cdata_ax, l2x_ax , &
                                     fractions_l=fractions_lx, fractions_a=fractions_ax, &
                                     fluxlist=seq_flds_l2x_fluxes, statelist=seq_flds_l2x_states )
               call t_drvstopf  ('driver_atmprep_lnd2atm')
            endif
            call t_drvstartf ('driver_atmprep_mrgx2a',barrier=mpicom_CPLID)
            call mrg_x2a_run_mct( cdata_ax, l2x_ax, o2x_ax, xao_ax, i2x_ax, fractions_ax, x2a_ax )
            call t_drvstopf  ('driver_atmprep_mrgx2a')

            if (info_debug > 1) then
               call t_drvstartf ('driver_atmprep_diagav',barrier=mpicom_CPLID)
               call seq_diag_avect_mct(cdata_ax,x2a_ax,'send atm')
               call t_drvstopf  ('driver_atmprep_diagav')
            endif
         endif  ! atm_prognostic
         call t_drvstopf  ('DRIVER_ATMPREP',cplrun=.true.)
         if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
         CALL POP_MODULEID()
		 endif  ! CPLID

         !----------------------------------------------------------
         ! cpl -> atm
         !----------------------------------------------------------

         if (iamin_CPLATMID .and. atm_prognostic) then
            CALL PUSH_MODULEID(MODULE_CPLATM)
			call t_drvstartf ('DRIVER_C2A',barrier=mpicom_CPLATMID)
            call t_drvstartf ('driver_c2a_atmx2atma',barrier=mpicom_CPLATMID)
            call map_atmx2atma_mct( cdata_ax, x2a_ax, cdata_aa, x2a_aa)
            call t_drvstopf  ('driver_c2a_atmx2atma')
            call t_drvstartf ('driver_c2a_infoexch',barrier=mpicom_CPLATMID)
            call seq_infodata_exchange(infodata,CPLATMID,'cpl2atm_run')
            call t_drvstopf  ('driver_c2a_infoexch')
            call t_drvstopf  ('DRIVER_C2A')
            CALL POP_MODULEID()
		 endif

      endif

      !----------------------------------------------------------
      ! RUN atm model, phase = 1, juanxiong he
      !----------------------------------------------------------

      if (atm_present .and. atmrun_alarm .and. iamin_ATMID) then
         CALL PUSH_MODULEID(MODULE_ATM)
		 if (run_barriers) then
            call t_drvstartf ('DRIVER_ATM_RUN_BARRIER')
            call mpi_barrier(mpicom_ATMID,ierr)
            call t_drvstopf ('DRIVER_ATM_RUN_BARRIER')
         endif
         call t_drvstartf ('DRIVER_ATM_RUN',barrier=mpicom_ATMID)
         if (drv_threading) call seq_comm_setnthreads(nthreads_ATMID)
         if (atm_prognostic) call mct_avect_vecmult(x2a_aa,drv2mdl_aa,seq_flds_x2a_fluxes)
!wangty modify
#ifdef wrf
         integration_phase = 1 !juanxiong he
         call atm_run_mct( EClock_a, EClock_w, cdata_aa, cdata_cc, cdata_caca, x2a_aa, a2x_aa, &
                           x2c_cc1, x2c_cc2, c2x_cc1, c2x_cc2, &
                           x2ca_caca1, x2ca_caca2, ca2x_caca1, ca2x_caca2, &
                           twoway_coupling, twoway_nudging, integration_phase ) !juanxiong he
#else
         call atm_run_mct( EClock_a, cdata_aa, x2a_aa, a2x_aa)
#endif
         call mct_avect_vecmult(a2x_aa,mdl2drv_aa,seq_flds_a2x_fluxes)
         if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
         call t_drvstopf  ('DRIVER_ATM_RUN')
         CALL POP_MODULEID()
	  endif

      !----------------------------------------------------------
      ! Run Glc Model
      !----------------------------------------------------------

      if (glc_present .and. glcrun_alarm .and. iamin_GLCID) then
         CALL PUSH_MODULEID(MODULE_GLC)
		 if (run_barriers) then
            call t_drvstartf ('DRIVER_GLC_RUN_BARRIER')
            call mpi_barrier(mpicom_GLCID,ierr)
            call t_drvstopf ('DRIVER_GLC_RUN_BARRIER')
         endif
         call t_drvstartf ('DRIVER_GLC_RUN',barrier=mpicom_GLCID)
         if (drv_threading) call seq_comm_setnthreads(nthreads_GLCID)
         if (glc_prognostic) call mct_avect_vecmult(x2g_gg,drv2mdl_gg,seq_flds_x2g_fluxes)
         call glc_run_mct( EClock_g, cdata_gg, x2g_gg, g2x_gg)
         call mct_avect_vecmult(g2x_gg,mdl2drv_gg,seq_flds_g2x_fluxes)
         if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
         call t_drvstopf  ('DRIVER_GLC_RUN')
         CALL POP_MODULEID()
	  endif
 
      !----------------------------------------------------------
      ! glc -> cpl
      !----------------------------------------------------------

      if (glc_present .and. sno_prognostic .and. glcrun_alarm) then

         if (iamin_CPLGLCID) then
		    CALL PUSH_MODULEID(MODULE_CPLGLC)
            call t_drvstartf ('DRIVER_G2C',barrier=mpicom_CPLGLCID)
            call t_drvstartf ('driver_g2c_glcg2glcx',barrier=mpicom_CPLGLCID)
            call map_glcg2glcx_mct( cdata_gg, g2x_gg, cdata_gx, g2x_gx)
            call t_drvstopf  ('driver_g2c_glcg2glcx')
            call t_drvstartf ('driver_g2c_infoexch',barrier=mpicom_CPLGLCID)
            call seq_infodata_exchange(infodata,CPLGLCID,'glc2cpl_run')
            call t_drvstopf  ('driver_g2c_infoexch')
            call t_drvstopf  ('DRIVER_G2C')
            CALL POP_MODULEID()
		 endif

         if (iamin_CPLID) then
		    CALL PUSH_MODULEID(MODULE_CPL)
            call t_drvstartf  ('DRIVER_GLCPOST',cplrun=.true.,barrier=mpicom_CPLID)
            if (drv_threading) call seq_comm_setnthreads(nthreads_CPLID)
            if (info_debug > 1) then
               call t_drvstartf ('driver_glcpost_diagav',barrier=mpicom_CPLID)
               call seq_diag_avect_mct(cdata_gx,g2x_gx,'recv glc')
               call t_drvstopf  ('driver_glcpost_diagav')
            endif
            call t_drvstartf ('driver_glcpost_glc2sno',barrier=mpicom_CPLID)
            call map_glc2sno_mct( cdata_gx, g2x_gx, cdata_sx, g2x_sx )
            call t_drvstopf  ('driver_glcpost_glc2sno')
            call t_drvstartf ('driver_glcpost_mrgx2s',barrier=mpicom_CPLID)
            call mrg_x2s_run_mct( cdata_sx, g2x_sx, x2s_sx )
            call t_drvstopf  ('driver_glcpost_mrgx2s')
            if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
            call t_drvstopf  ('DRIVER_GLCPOST',cplrun=.true.)
            CALL POP_MODULEID()
		 endif

      endif   ! run alarm, glc_present
!wangty modify
#ifdef wrf
      !----------------------------------------------------------
      ! atm -> cpl for wrf, juangxiong he 
      !----------------------------------------------------------
      if (atm_present .and. atmrun_alarm) then
         if (iamin_CPLATMID) then
		    CALL PUSH_MODULEID(MODULE_CPLATM)
            call t_drvstartf ('DRIVER_A2C',barrier=mpicom_CPLATMID)
            call t_drvstartf ('driver_a2c_atma2atmx',barrier=mpicom_CPLATMID)
            call map_cama2camx_mct(cdata_cc, c2x_cc1, cdata_cx, c2x_cx1) !juanxiong he
            call map_cama2camx_mct(cdata_cc, c2x_cc2, cdata_cx, c2x_cx2) !juanxiong he
            call t_drvstopf  ('driver_a2c_atma2atmx')
            call t_drvstartf ('driver_a2c_infoexch',barrier=mpicom_CPLATMID)
            call seq_infodata_exchange(infodata,CPLATMID,'atm2cpl_run')
            call t_drvstopf  ('driver_a2c_infoexch')
            call t_drvstopf  ('DRIVER_A2C')
            CALL POP_MODULEID()
		 endif
      endif ! run alarm

     !juanxiong he
     if (wrf_present .and. wrfrun_alarm) then

         !----------------------------------------------------------
         ! wrf prep
         !----------------------------------------------------------

         if (iamin_CPLID) then
		 CALL PUSH_MODULEID(MODULE_CPL)
         if (drv_threading) call seq_comm_setnthreads(nthreads_CPLID)
         call t_drvstartf ('DRIVER_WRFPREP',cplrun=.true.,barrier=mpicom_CPLID)

         call t_drvstartf ('driver_wrfprep_cam2wrf',barrier=mpicom_CPLID)
         call map_cam2wrf_mct( cdata_cx, c2x_cx1, cdata_mx, c2x_mx1 , &
                                    statelist=seq_flds_c2x_states )
         call map_cam2wrf_mct( cdata_cx, c2x_cx2, cdata_mx, c2x_mx2 , &
                                    statelist=seq_flds_c2x_states )
         call t_drvstopf  ('driver_wrfprep_cam2wrf')

         if ( seq_comm_iamroot(CPLID)) write(logunit,F00) 'Calling mrg_x2w_run_mct'
         call mrg_x2w_run_mct( cdata_mx, c2x_mx1, x2m_mx1)
         call mrg_x2w_run_mct( cdata_mx, c2x_mx2, x2m_mx2)

         call t_drvstopf  ('DRIVER_WRFPREP',cplrun=.true.)
         if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
         CALL POP_MODULEID()
		 endif  ! CPLID

         !----------------------------------------------------------
         ! cpl -> wrf, 3d
         !----------------------------------------------------------

         if (iamin_CPLWRFID .and. wrf_prognostic) then
            CALL PUSH_MODULEID(MODULE_CPLWRF)
			call t_drvstartf ('DRIVER_C2W',barrier=mpicom_CPLWRFID)
            call t_drvstartf ('driver_c2w_wrfx2wrfa',barrier=mpicom_CPLWRFID)
            call map_wrfx2wrfw_mct( cdata_mx, x2m_mx1, cdata_mm, x2m_mm1)   ! juaxniong he
            call map_wrfx2wrfw_mct( cdata_mx, x2m_mx2, cdata_mm, x2m_mm2)   ! juaxniong he
            call t_drvstopf  ('driver_c2w_wrfx2wrfa')
            call t_drvstartf ('driver_c2w_infoexch',barrier=mpicom_CPLWRFID)
            call seq_infodata_exchange(infodata,CPLWRFID,'cpl2wrf_run')
            call t_drvstopf  ('driver_c2w_infoexch')
            call t_drvstopf  ('DRIVER_C2W')
            CALL POP_MODULEID()
		 endif

      endif

      !----------------------------------------------------------
      ! RUN wrf model
      !----------------------------------------------------------

      if (wrf_present .and. wrfrun_alarm .and. iamin_WRFID) then
         CALL PUSH_MODULEID(MODULE_WRF)
		 call t_drvstartf ('DRIVER_WRF_RUN',barrier=mpicom_WRFID)
         if (drv_threading) call seq_comm_setnthreads(nthreads_WRFID)
         call wrf_run_mct( EClock_a, EClock_w, cdata_ww, cdata_mm, x2w_ww, w2x_ww, x2m_mm1, &
                           x2m_mm2, m2x_mm, twoway_coupling, twoway_nudging ) !juanxiong he
         if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
         call t_drvstopf  ('DRIVER_WRF_RUN')
         CALL POP_MODULEID()
	  endif

      !----------------------------------------------------------
      ! wrf -> cpl
      !----------------------------------------------------------
      if (wrf_present) then
         if (iamin_CPLWRFID.and.twoway_coupling) then
		    CALL PUSH_MODULEID(MODULE_CPLWRF)
            call t_drvstartf ('DRIVER_M2X',barrier=mpicom_CPLWRFID)
            call t_drvstartf ('driver_m2x_wrfw2wrfx',barrier=mpicom_CPLWRFID)
            call map_wrfw2wrfx_mct(cdata_mm, m2x_mm, cdata_mx, m2x_mx) !juanxiong he
            call t_drvstopf  ('driver_m2x_wrfw2wrfx')
            call t_drvstartf ('driver_m2x_infoexch',barrier=mpicom_CPLWRFID)
            call seq_infodata_exchange(infodata,CPLWRFID,'wrf2cpl_run')
            call t_drvstopf  ('driver_m2x_infoexch')
            call t_drvstopf  ('DRIVER_M2X')
            CALL POP_MODULEID()
		 endif

         if (iamin_CPLID) then
		    CALL PUSH_MODULEID(MODULE_CPL)
            call t_drvstartf ('DRIVER_WRFPOST',cplrun=.true.,barrier=mpicom_CPLID)
            if (drv_threading) call seq_comm_setnthreads(nthreads_CPLID)
            if (info_debug > 1) then
               call t_drvstartf ('driver_wrfpost_diagav',barrier=mpicom_CPLID)
               call seq_diag_avect_mct(cdata_mx,m2x_mx,'recv wrf')
               call t_drvstopf  ('driver_wrfpost_diagav')
            endif
            if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
            call t_drvstopf  ('DRIVER_WRFPOST',cplrun=.true.)
            CALL POP_MODULEID()
		 endif
      endif
      !----------------------------------------------------------
      ! budget with new fractions
      !----------------------------------------------------------

      !----------------------------------------------------------
      ! atm -> cpl for geatm, juanxiong he
      !----------------------------------------------------------
      if (atm_present .and. atmrun_alarm) then
         if (iamin_CPLATMID) then
		    CALL PUSH_MODULEID(MODULE_CPLATM)
            call t_drvstartf ('DRIVER_A2C',barrier=mpicom_CPLATMID)
            call t_drvstartf ('driver_a2ca_gatma2atmx',barrier=mpicom_CPLATMID)
            call map_gcama2camx_mct(cdata_caca, ca2x_caca1, cdata_cax, ca2x_cax1)  !juanxiong he
            call map_gcama2camx_mct(cdata_caca, ca2x_caca2, cdata_cax, ca2x_cax2)  !juanxiong he
            call t_drvstopf  ('driver_a2ca_gatma2atmx')
            call t_drvstartf ('driver_a2ca_infoexch',barrier=mpicom_CPLATMID)
            call seq_infodata_exchange(infodata,CPLATMID,'atm2cpl_run')
            call t_drvstopf  ('driver_a2ca_infoexch')
            call t_drvstopf  ('DRIVER_A2C')
            CALL POP_MODULEID()
		 endif
      endif ! run alarm

     !juanxiong he
     if (geatm_present .and. gearun_alarm) then

         !----------------------------------------------------------
         ! gea prep
         !----------------------------------------------------------

         if (iamin_CPLID) then
		 CALL PUSH_MODULEID(MODULE_CPL)
         if (drv_threading) call seq_comm_setnthreads(nthreads_CPLID)
         call t_drvstartf ('DRIVER_GEAPREP',cplrun=.true.,barrier=mpicom_CPLID)

         call t_drvstartf ('driver_geaprep_cam2gea',barrier=mpicom_CPLID)
         call map_cam2gea_mct( cdata_cax, ca2x_cax1, cdata_gex, ca2x_chemx1 , &
                               statelist=seq_flds_ca2x_states )
         call map_cam2gea_mct( cdata_cax, ca2x_cax2, cdata_gex, ca2x_chemx2 , &
                               statelist=seq_flds_ca2x_states )
         call t_drvstopf  ('driver_geaprep_cam2gea')

         if ( seq_comm_iamroot(CPLID)) write(logunit,F00) 'Calling mrg_x2w_run_mct'
         call mrg_x2ge_run_mct( cdata_gex, ca2x_chemx1, x2chem_chemx1)
         call mrg_x2ge_run_mct( cdata_gex, ca2x_chemx2, x2chem_chemx2)

         call t_drvstopf  ('DRIVER_GEAPREP',cplrun=.true.)
         if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
         CALL POP_MODULEID()
		 endif  ! CPLID

         !----------------------------------------------------------
         ! cpl -> gea, 3d
         !----------------------------------------------------------

         if (iamin_CPLGEAID .and. geatm_prognostic) then
            CALL PUSH_MODULEID(MODULE_CPLGEA)
			call t_drvstartf ('DRIVER_CA2GE',barrier=mpicom_CPLGEAID)
            call t_drvstartf ('driver_ca2ge_geax2geaa',barrier=mpicom_CPLGEAID)
            call map_geax2geaw_mct( cdata_gex, x2chem_chemx1, cdata_gege, x2chem_chemchem1)   ! juaxniong he
            call map_geax2geaw_mct( cdata_gex, x2chem_chemx2, cdata_gege, x2chem_chemchem2)   ! juaxniong he
            call t_drvstopf  ('driver_ca2ge_geax2geaa')
            call t_drvstartf ('driver_ca2ge_infoexch',barrier=mpicom_CPLGEAID)
            call seq_infodata_exchange(infodata,CPLGEAID,'cpl2gea_run')
            call t_drvstopf  ('driver_ca2ge_infoexch')
            call t_drvstopf  ('DRIVER_CA2GE')
            CALL POP_MODULEID()
		 endif
      endif

      !----------------------------------------------------------
      ! RUN geatm model
      !----------------------------------------------------------

      if (geatm_present .and. gearun_alarm .and. iamin_GEAID) then
         CALL PUSH_MODULEID(MODULE_GEA)
		 call t_drvstartf ('DRIVER_GEA_RUN',barrier=mpicom_GEAID)
         if (drv_threading) call seq_comm_setnthreads(nthreads_GEAID)
         call geatm_run_mct( EClock_a, EClock_ge, cdata_gege, &
                             x2chem_chemchem1, x2chem_chemchem2, chem2x_chemchem ) !juanxiong he
         if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
         call t_drvstopf  ('DRIVER_GEA_RUN')
         CALL POP_MODULEID()
	  endif

      !----------------------------------------------------------
      ! geatm -> cpl
      !----------------------------------------------------------
      if (geatm_present) then
         if (iamin_CPLGEAID.and.twoway_coupling) then
		    CALL PUSH_MODULEID(MODULE_CPLGEA)
            call t_drvstartf ('DRIVER_GEA2X',barrier=mpicom_CPLGEAID)
            call t_drvstartf ('driver_chem2x_geaw2geax',barrier=mpicom_CPLGEAID)
            call map_geaw2geax_mct(cdata_gege, chem2x_chemchem, cdata_gex, chem2x_chemx)  !juanxiong he
            call t_drvstopf  ('driver_chem2x_geaw2geax')
            call t_drvstartf ('driver_chem2x_infoexch',barrier=mpicom_CPLGEAID)
            call seq_infodata_exchange(infodata,CPLGEAID,'gea2cpl_run')
            call t_drvstopf  ('driver_chem2x_infoexch')
            call t_drvstopf  ('DRIVER_GEA2X')
            CALL POP_MODULEID()
		 endif

         if (iamin_CPLID) then
		    CALL PUSH_MODULEID(MODULE_CPL)
            call t_drvstartf ('DRIVER_GEAPOST',cplrun=.true.,barrier=mpicom_CPLID)
            if (drv_threading) call seq_comm_setnthreads(nthreads_CPLID)
            if (info_debug > 1) then
               call t_drvstartf ('driver_geapost_diagav',barrier=mpicom_CPLID)
               call seq_diag_avect_mct(cdata_gex,chem2x_chemx,'recv geatm')
               call t_drvstopf  ('driver_geapost_diagav')
            endif
            if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
            call t_drvstopf  ('DRIVER_GEAPOST',cplrun=.true.)
            CALL POP_MODULEID()
		 endif
      endif
      !----------------------------------------------------------
      ! RUN atm model, phase = 2, juanxiong he
      !----------------------------------------------------------

         !----------------------------------------------------------
         ! wrf -> cpl -> atm
         !----------------------------------------------------------

        if (iamin_CPLID.and.twoway_coupling) then
			 CALL PUSH_MODULEID(MODULE_CPL)
             ! wrf->cpl, juanxiong he
             if (wrf_present) then
               call t_drvstartf ('driver_atmprep_wrf2atm',barrier=mpicom_CPLID)
               call map_wrf2cam_mct( cdata_mx, m2x_mx, cdata_cx, m2x_cx , &
                                     fluxlist=seq_flds_w2x_fluxes, statelist=seq_flds_w2x_states )
               call t_drvstopf  ('driver_atmprep_wrf2atm')
            endif
            call t_drvstartf ('driver_atmprep_mrgx2c',barrier=mpicom_CPLID)
            if ( seq_comm_iamroot(CPLID)) write(logunit,F00) 'Calling mrg_x2c_run_mct'
            call mrg_x2c_run_mct( cdata_cx, m2x_cx, x2c_cx1 )
            call t_drvstopf  ('driver_atmprep_mrgx2c')
            CALL POP_MODULEID()
		 endif

         if (iamin_CPLATMID .and. atm_prognostic.and.twoway_coupling) then
            !cpl->cam, juanxiong he
			CALL PUSH_MODULEID(MODULE_CPLATM)
            call t_drvstartf ('DRIVER_C2A',barrier=mpicom_CPLATMID)
            call t_drvstartf ('driver_c2a_atmx2atma',barrier=mpicom_CPLATMID)
            call map_camx2cama_mct( cdata_cx, x2c_cx1, cdata_cc, x2c_cc1)
            call t_drvstopf  ('driver_c2a_atmx2atma')

            call t_drvstartf ('driver_c2a_infoexch',barrier=mpicom_CPLATMID)
            call seq_infodata_exchange(infodata,CPLATMID,'cpl2atm_run')
            call t_drvstopf  ('driver_c2a_infoexch')
            call t_drvstopf  ('DRIVER_C2A')
            CALL POP_MODULEID()
		 endif
      if (atm_present .and. atmrun_alarm .and. iamin_ATMID) then
         CALL PUSH_MODULEID(MODULE_ATM)
		 call t_drvstartf ('DRIVER_ATM_RUN',barrier=mpicom_ATMID)
         if (drv_threading) call seq_comm_setnthreads(nthreads_ATMID)
         integration_phase = 2 !juanxiong he
         call atm_run_mct( EClock_a, EClock_w, cdata_aa, cdata_cc, cdata_caca, x2a_aa, a2x_aa, &
                           x2c_cc1, x2c_cc2, c2x_cc1, c2x_cc2, &
                           x2ca_caca1, x2ca_caca2, ca2x_caca1, ca2x_caca2, &
                           twoway_coupling, twoway_nudging, integration_phase )
         call mct_avect_vecmult(a2x_aa,mdl2drv_aa,seq_flds_a2x_fluxes)
         if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
         call t_drvstopf  ('DRIVER_ATM_RUN')
         CALL POP_MODULEID()
	  endif

      !----------------------------------------------------------
      ! atm -> cpl for ccsm, juanxiong he
      !----------------------------------------------------------
#endif
      if (atm_present .and. atmrun_alarm) then
         if (iamin_CPLATMID) then
		    CALL PUSH_MODULEID(MODULE_CPLATM)
            call t_drvstartf ('DRIVER_A2C',barrier=mpicom_CPLATMID)
            call t_drvstartf ('driver_a2c_atma2atmx',barrier=mpicom_CPLATMID)
            call map_atma2atmx_mct( cdata_aa, a2x_aa, cdata_ax, a2x_ax)
            call t_drvstopf  ('driver_a2c_atma2atmx')
            call t_drvstartf ('driver_a2c_infoexch',barrier=mpicom_CPLATMID)
            call seq_infodata_exchange(infodata,CPLATMID,'atm2cpl_run')
            call t_drvstopf  ('driver_a2c_infoexch')
            call t_drvstopf  ('DRIVER_A2C')
            CALL POP_MODULEID()
		 endif

         if (iamin_CPLID) then
		    CALL PUSH_MODULEID(MODULE_CPL)
            call t_drvstartf ('DRIVER_ATMPOST',cplrun=.true.,barrier=mpicom_CPLID)
            if (drv_threading) call seq_comm_setnthreads(nthreads_CPLID)
            if (info_debug > 1) then
               call t_drvstartf ('driver_atmpost_diagav',barrier=mpicom_CPLID)
               call seq_diag_avect_mct(cdata_ax,a2x_ax,'recv atm')
               call t_drvstopf  ('driver_atmpost_diagav')
            endif
            if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
            call t_drvstopf  ('DRIVER_ATMPOST',cplrun=.true.)
            CALL POP_MODULEID()
		 endif
      
      endif ! run alarm

      !----------------------------------------------------------
      ! budget with new fractions
      !----------------------------------------------------------

#if (defined NEW_BUDGET)
      if (iamin_CPLID .and. do_budgets) then
	     CALL PUSH_MODULEID(MODULE_CPL)
         call t_drvstartf ('DRIVER_BUDGET2',cplrun=.true.,budget=.true.,barrier=mpicom_CPLID)
         if (atm_present) then
            call seq_diag_atm_mct(dom_ax, fractions_ax, a2x_a=a2x_ax, x2a_a=x2a_ax)
         endif
         if (ice_present) then
            call seq_diag_ice_mct(dom_ix, fractions_ix, i2x_i=i2x_ix)
         endif
         call t_drvstopf  ('DRIVER_BUDGET2',cplrun=.true.,budget=.true.)
         CALL POP_MODULEID()
 	  endif
      if (iamin_CPLID .and. do_budgets) then
         CALL PUSH_MODULEID(MODULE_CPL)
		 call t_drvstartf ('DRIVER_BUDGET3',cplrun=.true.,budget=.true.,barrier=mpicom_CPLID)
         call seq_diag_accum_mct()
         call t_drvstopf  ('DRIVER_BUDGET3',cplrun=.true.,budget=.true.)
         CALL POP_MODULEID()
	  endif
      if (iamin_CPLID .and. do_budgets) then
	     CALL PUSH_MODULEID(MODULE_CPL)
         call t_drvstartf ('DRIVER_BUDGETF',cplrun=.true.,budget=.true.,barrier=mpicom_CPLID)
         if (.not. dead_comps) call seq_diag_print_mct(EClock_d,stop_alarm,budget_inst, &
            budget_daily, budget_month, budget_ann, budget_ltann, budget_ltend)
         call seq_diag_zero_mct(EClock=EClock_d)
         call t_drvstopf  ('DRIVER_BUDGETF',cplrun=.true.,budget=.true.)
         CALL POP_MODULEID()
	  endif
#endif

      !----------------------------------------------------------
      ! ocn -> cpl, loose coupling (concurrent type mode)
      !----------------------------------------------------------

      if (.not.ocean_tight_coupling) then
      if (ocn_present .and. ocnnext_alarm) then
         if (iamin_CPLOCNID) then
		    CALL PUSH_MODULEID(MODULE_CPLOCN)
            call t_drvstartf ('DRIVER_O2C',barrier=mpicom_CPLOCNID)
            call t_drvstartf ('driver_o2c_ocno2ocnx',barrier=mpicom_CPLOCNID)
            call map_ocno2ocnx_mct( cdata_oo, o2x_oo, cdata_ox, o2x_ox)
            call t_drvstopf  ('driver_o2c_ocno2ocnx')
            call t_drvstartf ('driver_o2c_infoexch',barrier=mpicom_CPLOCNID)
            call seq_infodata_exchange(infodata,CPLOCNID,'ocn2cpl_run')
            call t_drvstopf  ('driver_o2c_infoexch')
            call t_drvstopf  ('DRIVER_O2C')
            CALL POP_MODULEID()
		 endif
         if (iamin_CPLID) then
		    CALL PUSH_MODULEID(MODULE_CPL)
            call t_drvstartf  ('DRIVER_OCNPOST',cplrun=.true.,barrier=mpicom_CPLID)
            if (drv_threading) call seq_comm_setnthreads(nthreads_CPLID)
            if (info_debug > 1) then
               call t_drvstartf ('driver_ocnpost_diagav',barrier=mpicom_CPLID)
               call seq_diag_avect_mct(cdata_ox,o2x_ox,'recv ocn')
               call t_drvstopf  ('driver_ocnpost_diagav')
            endif
            if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
            call t_drvstopf  ('DRIVER_OCNPOST',cplrun=.true.)
            CALL POP_MODULEID()
		 endif
      endif
      endif

      !----------------------------------------------------------
      ! Save driver level restart information
      !----------------------------------------------------------

      if ( restart_alarm .and. iamin_CPLID) then
	     CALL PUSH_MODULEID(MODULE_CPL)
         call t_drvstartf ('DRIVER_RESTART',cplrun=.true.,barrier=mpicom_CPLID)
         if (drv_threading) call seq_comm_setnthreads(nthreads_CPLID)
         if (iamroot_CPLID) then
		    CALL PUSH_MODULEID(MODULE_CPL)
            write(logunit,104) ' Write restart file at ',ymd,tod
            call shr_sys_flush(logunit)
			CALL POP_MODULEID()
         endif
         call seq_rest_write(EClock_d,seq_SyncClock)
         if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
         call t_drvstopf  ('DRIVER_RESTART',cplrun=.true.)
         CALL POP_MODULEID()
	  endif

      !----------------------------------------------------------
      ! Write history file, only AVs on CPLID
      !----------------------------------------------------------

      if (iamin_CPLID) then
         CALL PUSH_MODULEID(MODULE_CPL)
         call t_drvstartf ('DRIVER_HISTORY',cplrun=.true.,barrier=mpicom_CPLID)
         if ( history_alarm) then
            if (drv_threading) call seq_comm_setnthreads(nthreads_CPLID)
            if (iamroot_CPLID) then
			   CALL PUSH_MODULEID(MODULE_CPL)
               write(logunit,104) ' Write history file at ',ymd,tod
               call shr_sys_flush(logunit)
			   CALL POP_MODULEID()
            endif
            call seq_hist_write(EClock_d)
            if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
         endif

         if (do_histavg) then
            call seq_hist_writeavg(EClock_d,histavg_alarm)
         endif

         if (do_hist_a2x) then
            if (trim(hist_a2x_flds) == 'all') then
               call seq_hist_writeaux(EClock_d,'a2x','doma',cdata_ax,a2x_ax,atm_nx,atm_ny,ncpl)
            else
               call seq_hist_writeaux(EClock_d,'a2x','doma',cdata_ax,a2x_ax,atm_nx,atm_ny,ncpl,&
                                                flds=hist_a2x_flds)
            endif
         endif
         if (do_hist_a2x3hr) then
            if (trim(hist_a2x3hr_flds) == 'all') then
               call seq_hist_writeaux(EClock_d,'a2x3h','doma',cdata_ax,a2x_ax,atm_nx,atm_ny,8,t3hr_alarm)
            else
               call seq_hist_writeaux(EClock_d,'a2x3h','doma',cdata_ax,a2x_ax,atm_nx,atm_ny,8,t3hr_alarm,&
                                                 flds=hist_a2x3hr_flds)
            end if
         endif
         if (do_hist_a2x3hrp) then
            if (trim(hist_a2x3hrp_flds) == 'all') then
               call seq_hist_writeaux(EClock_d,'a2x3h_prec','doma',cdata_ax,a2x_ax,atm_nx,atm_ny,8,t3hr_alarm)
            else
               call seq_hist_writeaux(EClock_d,'a2x3h_prec','doma',cdata_ax,a2x_ax,atm_nx,atm_ny,8,t3hr_alarm,&
                                              flds=hist_a2x3hrp_flds)
            end if
         endif
         if (do_hist_a2x24hr) then
            call seq_hist_writeaux(EClock_d,'a2x1d','doma',cdata_ax,a2x_ax,atm_nx,atm_ny,1,t24hr_alarm)
         endif
         if (do_hist_l2x) then
            call seq_hist_writeaux(EClock_d,'l2x','doml',cdata_lx,l2x_lx,lnd_nx,lnd_ny,ncpl)
         endif
         call t_drvstopf  ('DRIVER_HISTORY',cplrun=.true.)
         CALL POP_MODULEID()
      end if

      ! --- End timestep clock/timing diagnostics
      call t_drvstartf ('DRIVER_TSTAMP_WRITE',cplrun=.true.)
      if (tod == 0 .or. info_debug > 1) then
         if (iamroot_CPLID) then
		    CALL PUSH_MODULEID(MODULE_CPL)
            call date_and_time(dstr,tstr)
            Time_estep = mpi_wtime()
            dtstep = time_estep-time_bstep
            dtstep_acc = dtstep_acc + dtstep
            dtstep_cnt = dtstep_cnt + 1
            write(logunit,101) ' tStamp_write: model date = ',ymd,tod, &
               ' wall clock = ',dstr(1:4),'-',dstr(5:6),'-',dstr(7:8),' ',&
                                tstr(1:2),':',tstr(3:4),':',tstr(5:6), &
               ' avg dt = ',dtstep_acc/dtstep_cnt,' dt = ',dtstep 
            Time_bstep = mpi_wtime()
            call shr_sys_flush(logunit)
			CALL POP_MODULEID()
         endif
      endif
      if (tod == 0) then
         if (iamroot_CPLID .or. iamroot_OCNID .or. iamroot_ATMID .or. &
             iamroot_LNDID .or. iamroot_ICEID .or. iamroot_GLCID) then
            call shr_mem_getusage(msize,mrss)
            write(logunit,105) ' memory_write: model date = ',ymd,tod, &
               ' memory = ',mrss,' MB (highwater)    ',msize,' MB (usage)', &
               '  (pe=',iam_GLOID,' comps=',trim(complist)//')'
         endif
      endif
      if (info_debug > 1) then
         if (iamroot_CPLID) then
		    CALL PUSH_MODULEID(MODULE_CPL)
            call seq_infodata_GetData(infodata,nextsw_cday=nextsw_cday)
!            write(logunit,106) ' nextsw_cday = ',nextsw_cday
            write(logunit,*) '  nextsw_cday = ',nextsw_cday
            CALL POP_MODULEID()
		 endif
      endif
      call t_drvstopf  ('DRIVER_TSTAMP_WRITE',cplrun=.true.)

      call t_stopf  ('DRIVER_RUN_LOOP')
      ! --- Write out performance data 
      call t_drvstartf  ('DRIVER_TPROF_WRITE',cplrun=.true.)
      if (tprof_alarm) then
         call t_startf("sync1_tprof")
         call mpi_barrier(mpicom_GLOID,ierr)
         call t_stopf("sync1_tprof")

         write(timing_file,'(a,i8.8,a1,i5.5)') trim(tchkpt_dir)//"/ccsm_timing_",ymd,"_",tod
         call t_prf(filename=trim(timing_file), mpicom=mpicom_GLOID, &
                    num_outpe=1)

         call t_startf("sync2_tprof")
         call mpi_barrier(mpicom_GLOID,ierr)
         call t_stopf("sync2_tprof")
      endif
      call t_drvstopf  ('DRIVER_TPROF_WRITE',cplrun=.true.)

   end do   ! driver run loop

   call t_startf ('DRIVER_RUN_LOOP_BSTOP')
   call mpi_barrier(mpicom_GLOID,ierr)
   call t_stopf ('DRIVER_RUN_LOOP_BSTOP')

   Time_end = mpi_wtime()

   !----------------------------------------------------------
   ! Ending of basic time step loop
   !----------------------------------------------------------

end subroutine ccsm_run


!===============================================================================

subroutine ccsm_final()

   !------------------------------------------------------------------------
   ! Finalization of all models
   !------------------------------------------------------------------------

 103  format( 5A )
   ! TODO finalize routines need to be cleaned up 

   call t_barrierf ('DRIVER_FINAL_BARRIER', mpicom_GLOID)
   call t_startf ('DRIVER_FINAL')

   call seq_timemgr_EClockGetData( EClock_d, stepno=endstep)
   call shr_mem_getusage(msize,mrss)

   if (iamin_ATMID) then
      CALL PUSH_MODULEID(MODULE_ATM)
      if (drv_threading) call seq_comm_setnthreads(nthreads_ATMID)
      call atm_final_mct( )
      if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
      CALL POP_MODULEID()
   endif
!wangty modify
#ifdef wrf
   if (iamin_WRFID) then  !juanxiong he
      CALL PUSH_MODULEID(MODULE_WRF)
      if (drv_threading) call seq_comm_setnthreads(nthreads_WRFID)
      call wrf_final_mct( )
      if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
      CALL POP_MODULEID()
   endif
   if (iamin_GEAID) then  !juanxiong he
      CALL PUSH_MODULEID(MODULE_GEA)
      if (drv_threading) call seq_comm_setnthreads(nthreads_GEAID)
      call geatm_final_mct( )
      if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
      CALL POP_MODULEID()
   endif
#endif
   if (iamin_LNDID) then
      CALL PUSH_MODULEID(MODULE_LND)
      if (drv_threading) call seq_comm_setnthreads(nthreads_LNDID)
      call lnd_final_mct( )
      if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
      CALL POP_MODULEID()
   endif
   if (iamin_ICEID) then
      CALL PUSH_MODULEID(MODULE_ICE)
      if (drv_threading) call seq_comm_setnthreads(nthreads_ICEID)
      call ice_final_mct( )
      if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
      CALL POP_MODULEID()
   endif
   if (iamin_OCNID) then
      CALL PUSH_MODULEID(MODULE_OCN)
      if (drv_threading) call seq_comm_setnthreads(nthreads_OCNID)
      call ocn_final_mct( )
      if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
      CALL POP_MODULEID()
   endif
   if (iamin_GLCID) then
      CALL PUSH_MODULEID(MODULE_GLC)
      if (drv_threading) call seq_comm_setnthreads(nthreads_GLCID)
      call glc_final_mct( )
      if (drv_threading) call seq_comm_setnthreads(nthreads_GLOID)
      CALL POP_MODULEID()
   endif

   !------------------------------------------------------------------------
   ! End the run cleanly
   !------------------------------------------------------------------------

   call seq_io_finalize()
   
   call shr_mpi_min(msize,msize0,mpicom_GLOID,'driver msize0',all=.true.)
   call shr_mpi_max(msize,msize1,mpicom_GLOID,'driver msize1',all=.true.)
   call shr_mpi_min(mrss,mrss0,mpicom_GLOID,'driver mrss0',all=.true.)
   call shr_mpi_max(mrss,mrss1,mpicom_GLOID,'driver mrss1',all=.true.)
   if ( iamroot_CPLID )then
	  CALL PUSH_MODULEID(MODULE_CPL)
      call seq_timemgr_EClockGetData( EClock_d, curr_ymd=ymd, curr_tod=tod, dtime=dtime)
      write(logunit,'(//)')
      write(logunit,FormatA) subname, 'SUCCESSFUL TERMINATION OF CPL7-CCSM'
      write(logunit,FormatD) subname, '  at YMD,TOD = ',ymd,tod
      simDays = (endStep-begStep)*dtime/(24._r8*3600._r8)
      write(logunit,FormatR) subname, '# simulated days (this run) = ', simDays
      write(logunit,FormatR) subname, 'compute time (hrs)          = ', (Time_end-Time_begin)/3600._r8
      if ( (Time_end /= Time_begin) .and. (simDays /= 0.0_r8) )then
         SYPD = shr_const_cday*simDays/(days_per_year*(Time_end-Time_begin))
         write(logunit,FormatR) subname, '# simulated years / cmp-day = ', SYPD
      endif
      write(logunit,FormatR) subname,' pes min memory highwater  (MB)  = ',mrss0
      write(logunit,FormatR) subname,' pes max memory highwater  (MB)  = ',mrss1
      write(logunit,FormatR) subname,' pes min memory last usage (MB)  = ',msize0
      write(logunit,FormatR) subname,' pes max memory last usage (MB)  = ',msize1
      write(logunit,'(//)')
      close(logunit)
	  CALL POP_MODULEID()
   endif

   call t_stopf  ('DRIVER_FINAL')
   call t_prf(trim(timing_dir)//'/ccsm_timing', mpicom_GLOID)
   call t_finalizef()

end subroutine ccsm_final


!===============================================================================

subroutine t_drvstartf(string,cplrun,budget,barrier)

   implicit none

   character(len=*),intent(in) :: string
   logical,intent(in),optional :: cplrun
   logical,intent(in),optional :: budget
   integer,intent(in),optional :: barrier

   character(len=128) :: strbar
   character(len=*),parameter :: strcpl = 'DRIVER_CPL_RUN'
   character(len=*),parameter :: strbud = 'DRIVER_BUDGET'
   logical :: lcplrun,lbudget

!-------------------------------------------------------------------------------

   lcplrun  = .false.
   lbudget  = .false.
   if (present(cplrun)) then
      lcplrun = cplrun
   endif
   if (present(budget)) then
      lbudget = budget
   endif

   if (present(barrier)) then
      strbar = trim(string)//'_BARRIER'
      call t_barrierf (trim(strbar), barrier)
   endif

   if (lcplrun) then
      call t_startf   (trim(strcpl))
   endif

   if (lbudget) then
      call t_startf   (trim(strbud))
   endif

   call t_startf   (trim(string))

end subroutine t_drvstartf

!===============================================================================

subroutine t_drvstopf(string,cplrun,budget)

   implicit none

   character(len=*),intent(in) :: string
   logical,intent(in),optional :: cplrun
   logical,intent(in),optional :: budget

   character(len=128) :: strbar
   character(len=*),parameter :: strcpl = 'DRIVER_CPL_RUN'
   character(len=*),parameter :: strbud = 'DRIVER_BUDGET'
   logical :: lcplrun,lbudget

!-------------------------------------------------------------------------------

   lcplrun = .false.
   lbudget = .false.
   if (present(cplrun)) then
      lcplrun = cplrun
   endif
   if (present(budget)) then
      lbudget = budget
   endif

!  strbar = trim(string)//'_BARRIER'

   call t_stopf   (trim(string))

   if (lbudget) then
      call t_stopf   (trim(strbud))
   endif

   if (lcplrun) then
      call t_stopf   (trim(strcpl))
   endif

end subroutine t_drvstopf

!===============================================================================

subroutine seq_ccsm_printlogheader()

  !-----------------------------------------------------------------------
  !
  ! Purpose: Print basic information on what this driver program is
  ! to the logfile.
  !
  !-----------------------------------------------------------------------
  !
  ! Local variables
  !
  implicit none

  character(len=8) :: cdate          ! System date
  character(len=8) :: ctime          ! System time
  integer          :: values(8)
  character        :: date*8, time*10, zone*5 

!-------------------------------------------------------------------------------
   
  call date_and_time (date, time, zone, values) 
  cdate(1:2) = date(5:6) 
  cdate(3:3) = '/' 
  cdate(4:5) = date(7:8) 
  cdate(6:6) = '/' 
  cdate(7:8) = date(3:4) 
  ctime(1:2) = time(1:2) 
  ctime(3:3) = ':' 
  ctime(4:5) = time(3:4) 
  ctime(6:6) = ':' 
  ctime(7:8) = time(5:6) 
  write(logunit,F00) '------------------------------------------------------------'
  write(logunit,F00) '     NCAR CPL7 Community Climate System Model (CCSM)  '
  write(logunit,F00) '------------------------------------------------------------'
  write(logunit,F00) '     (Online documentation is available on the CCSM         '
  write(logunit,F00) '      Models page: http://www.ccsm.ucar.edu/models/         '
  write(logunit,F00) '      License information is available as a link from above '
  write(logunit,F00) '------------------------------------------------------------'
  write(logunit,F00) '                DATE ',cdate, ' TIME ', ctime
  write(logunit,F00) '------------------------------------------------------------'
  write(logunit,*)' '
  write(logunit,*)' '

end subroutine seq_ccsm_printlogheader


#ifdef ESMF_INTERFACE

!===============================================================================

subroutine ccsm_comp_init(comp, importState, exportState, clock, rc)
   type(ESMF_CplComp)   :: comp
   type(ESMF_State)     :: importState, exportState
   type(ESMF_Clock)     :: clock
   integer, intent(out) :: rc

   ! Local variables
   type(ESMF_State)    :: attState
   integer             :: localrc
   type(ESMF_GridComp) :: atmComp, lndComp, iceComp, ocnComp, glcComp
   type(ESMF_VM)       :: vm
   character(len=80)   :: str
   integer             :: rc2
   integer, dimension(1) :: rootList

   rc = ESMF_SUCCESS

   !------
   ! Create a state object to which the field level attributes will be 
   ! attached, and link the state to the specified component
   !------
   attState = ESMF_StateCreate(name="ccsm_atts", rc=localrc)
   if (localrc /= ESMF_SUCCESS) call shr_sys_abort('failed to create state for attributes')

   call ESMF_AttributeLink(comp, attState, rc=localrc)
   if (localrc /= ESMF_SUCCESS) call shr_sys_abort('failed to link attributes')

   !------
   ! Create and setup the model components
   !------
   call atm_register(atm_petlist, comp, atmComp)
   call lnd_register(lnd_petlist, comp, lndComp)
   call ice_register(ice_petlist, comp, iceComp)
   call ocn_register(ocn_petlist, comp, ocnComp)
   call glc_register(glc_petlist, comp, glcComp)

   !------
   ! Process the CESM initialization
   !------
   call ccsm_init()

   !------
   ! Set the application and field level attributes
   !------
   call esmfshr_attribute_appl_init(comp, rc=localrc)
   !call esmfshr_attribute_fields_init(attState, rc=localrc)

   !------
   ! Get the VM and root pet list to be used for the AttributeUpdate call
   !------
! get current
   !call ESMF_VMGetGlobal(vm, rc=localrc)
   call ESMF_VMGetCurrent(vm, rc=localrc)
   if (localrc /= 0) call shr_sys_abort('failed to get VM')

   !rootList = (/mpicom_GLOID/)
   rootList(1) = atm_petlist(1)

! use this one
   call ESMF_AttributeUpdate(atmComp, vm, rootList=atm_petlist, rc=localrc)
!   call ESMF_AttributeUpdate(atmComp, vm, rootList=rootList, rc=localrc)
! try using just first pet in petlist
! /= ESMF_SUCCESS
! Add ESMF_Finalize w/ abort
! Macro in ESMF_Attribute - #define DEBUG
   if (localrc /= ESMF_SUCCESS) then
      write(logunit,*) ' '
      write(logunit,*) 'KDS: Error updating atm attributes: ', localrc
      call ESMF_Finalize()
      call shr_sys_abort('failed to update atm attributes')
   endif

   call ESMF_AttributeUpdate(lndComp, vm, rootList=lnd_petlist, rc=localrc)
!   if (localrc /= 0) then
!      call ESMF_Finalize()
!      call shr_sys_abort('failed to update lnd attributes')
!   endif

   call ESMF_AttributeUpdate(iceComp, vm, rootList=ice_petlist, rc=localrc)
!   if (localrc /= 0) call shr_sys_abort('failed to update ice attributes')

   call ESMF_AttributeUpdate(ocnComp, vm, rootList=ocn_petlist, rc=localrc)
!   if (localrc /= 0) call shr_sys_abort('failed to update ocn attributes')

   call ESMF_AttributeUpdate(glcComp, vm, rootList=glc_petlist, rc=localrc)
!   if (localrc /= 0) call shr_sys_abort('failed to update glc attributes')

   !------
   ! Write out all of the attributes to the CIM compliant XML file
   !------
   if (iamroot_GLOID) then

      call ESMF_AttributeWrite( &
              comp, &
              convention='CIM 1.0', &
              purpose='Model Component Simulation Description', &
              attwriteflag=ESMF_ATTWRITE_XML, rc=localrc)

   endif

   rc = localrc

end subroutine ccsm_comp_init

!===============================================================================

subroutine ccsm_comp_run(comp, importState, exportState, clock, rc)
   type(ESMF_CplComp)   :: comp
   type(ESMF_State)     :: importState, exportState
   type(ESMF_Clock)     :: clock
   integer, intent(out) :: rc

   rc = ESMF_SUCCESS

   call ccsm_run()

end subroutine ccsm_comp_run

!===============================================================================

subroutine ccsm_comp_final(comp, importState, exportState, clock, rc)
   type(ESMF_CplComp)   :: comp
   type(ESMF_State)     :: importState, exportState
   type(ESMF_Clock)     :: clock
   integer, intent(out) :: rc

   rc = ESMF_SUCCESS

   call ccsm_final()

end subroutine ccsm_comp_final


!===============================================================================
!
! This subroutine registers the initialization, run and finalization routines
! for the specified coupler component.  
!
subroutine ccsm_comp_register(comp, rc)
     type(ESMF_CplComp) :: comp
     integer, intent(out) :: rc

   rc = ESMF_SUCCESS

   call ESMF_CplCompSetEntryPoint(comp, ESMF_SETINIT, &
                                  userRoutine=ccsm_comp_init, rc=rc)
   call ESMF_CplCompSetEntryPoint(comp, ESMF_SETRUN, &
                                  userRoutine=ccsm_comp_run, rc=rc)
   call ESMF_CplCompSetEntryPoint(comp, ESMF_SETFINAL, &
                                  userRoutine=ccsm_comp_final, rc=rc)

end subroutine ccsm_comp_register

!===============================================================================

#endif

end module ccsm_comp_mod

