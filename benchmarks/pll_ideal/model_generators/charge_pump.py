import pythams.core.block as blocklib
from pythams.core.expr import *
import pythams.core.intervals as intervallib
import pythams.core.fixedpoint as fxplib
import pythams.core.integer as intlib 
import pythams.core.rtl as rtllib 



class Charge_Pump_Generator:

    output_current_real_type = None
    
    def generate_block(input_voltage = 3.3, rel_prec = 0.01):
    
        charge_pump = blocklib.AMSBlock('charge_pump')

        up_param   = charge_pump.decl_param('up_current_param',   Constant(20e-5))
        down_param = charge_pump.decl_param('down_current_param', Constant(20e-5))

        input_up_digital   = charge_pump.decl_var('input_up_digital',   blocklib.VarKind.Input, DigitalType(1))
        input_down_digital = charge_pump.decl_var('input_down_digital', blocklib.VarKind.Input, DigitalType(1))
        
        output_current_real = charge_pump.decl_var('output_current_real', blocklib.VarKind.Output, \
                                                   intervallib.real_type_from_expr(charge_pump, Constant(input_voltage) * input_up_digital * up_param - Constant(input_voltage) * input_down_digital * down_param) )

        Charge_Pump_Generator.output_current_real_type = output_current_real.type
        charge_pump.decl_relation(VarAssign(output_current_real, up_param * input_up_digital + down_param * input_down_digital))
        return charge_pump
    
    

charge_pump_ams_block = Charge_Pump_Generator.generate_block()

if __name__ == "__main__":
    ival_reg = intervallib.compute_intervals_for_block(charge_pump_ams_block,rel_prec=0.01)

    fp_block = fxplib.to_fixed_point(ival_reg,charge_pump_ams_block)

    int_block = intlib.to_integer(fp_block)

    rtl_block = rtllib.RTLBlock(int_block,{}, name_override = 'charge_pump')

    rtl_block.generate_verilog_src('../')