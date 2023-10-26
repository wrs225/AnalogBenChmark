module phase_locked_loop(
input reference_clk_digital,
output output_clk_digital,

input clk, //Clock for event-driven simulator

input reset
);


logic [23:0] output_current_real;
logic [ 9:0] output_voltage_real;

logic        output_up_digital;
logic        output_down_digital;

logic        feedback_div_clk_digital;

charge_pump                  cpmp(.input_up_digital(output_up_digital),   
                                  .input_down_digital(output_down_digital), 
                                  .output_current_real(output_current_real), 
                                  .reset(reset),
                                  .clk(clk));

voltage_controlled_oscillator vco(.input_voltage_real(output_voltage_real), 
                                  .output_clk_digital(output_clock_digital),     
                                  .reset(reset),
                                  .clk(clk));

loop_filter                    lf(.input_current_real(output_current_real), 
                                  .output_voltage_real(output_voltage_real),
                                  .reset(reset),
                                  .clk(clk));

phase_frequency_detector      pfd(.input_reference_clock_digital(reference_clk_digital), 
                                  .input_feedback_clock_digital(feedback_div_clk_digital), 
                                  .output_up_digital(output_up_digital), 
                                  .output_down_digital(output_down_digital), 
                                  .reset(reset),
                                  .clk(clk));

frequency_divider              fd(.input_clock_digital(reference_clk_digital), 
                                  .output_clock_digital(feedback_div_clk_digital),
                                  .reset(reset),
                                  .clk(clk));



endmodule