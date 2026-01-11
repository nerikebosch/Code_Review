import java.io.*;
import java.io.IOException;
import java.util.*;


/**
 *  This class represensts a manager.
 *  // The Manager2 class implements the following requirements:
 * // 1/ The system should classify the patient's respiratory status based on oxygen saturation (O2) and respiration rate (RR) readings as low O2 (O2 < 88), fast breathing (RR > 20), or normal.
 * // 2/ The system should separately classify the patient's breathing frequency based on RR reading as normal (12-20 breaths per minute), suspicious (< 6 br/min), slow (6-12 br/min), or fast (> 20 br/min).
 * // 3/ The system should output both results for further processing.
 * @author nerike
 */
public class Manager2 {

    private static List<String> LOGS = new ArrayList<>();

    // Constants for weight range
    private static final double MIN_WEIGHT = 50;
    private static final double MAX_WEIGHT = 120;

    // Constants for respiration and oxygen saturation rates
    private static final double LOW_OXYGEN_SATURATION_RATE = 88;

    private static final double MAX_NORMAL_BREATHING_RATE = 20;
    private static final double MIN_NORMAL_BREATHING_RATE = 12;
    private static final double MIN_SLOW_BREATHING_RATE = 6;

    private static boolean debug = false;


    /**
     * This method classifies the respiratory status based on the oxygen saturation and respiration rate readings.
     * It checks based on if readings of low O2 (O2 < 88) will be fast breathing and readings of RR (RR > 20) are normal.
     *
     * @param patient - Object containing information of the patient.
     * @param respirationRate - The patients breath per minute.
     * @param oxygenSaturation - The patients oxygen saturation percentage.
     * @return - Returns a string that tells the respiratory status if it is Ok, Fast Breathing or Low O2.
     */
    public String classifyRespiratoryStatus(Patient patient, int respirationRate, double oxygenSaturation) {
        String last_stat = null;

        if (patient.w < MIN_WEIGHT || patient.w > MAX_WEIGHT) {
            System.out.println("Suspicious weight!");
            LOGS.add("Invalid weight for " + patient.patient_name);
        }

        if (oxygenSaturation < LOW_OXYGEN_SATURATION_RATE) {
            last_stat = "LOW O2";
        } else if (respirationRate > MAX_NORMAL_BREATHING_RATE) {
            last_stat = "FAST BREATHING";
        } else {
            last_stat = "OK";
        }

        LOGS.add("Processed " + patient.patient_name);
        return last_stat;
    }

    /**
     *  Representing the breathing frequency rates
     */
    enum BreathingFrequency {
        SUSPICIOUS,
        SLOW,
        FAST,
        NORMAL
    }


    /**
     * This method classifies the breathing frequency based on some rates.
     * It should be based on RR reading as normal (12-20 breaths per minute), suspicious (< 6 br/min), slow (6-12 br/min), or fast (> 20 br/min).
     *
     * @param patient - Object containing information about the patient.
     * @param respirationRate - The patients breath per minute.
     * @param print - It prints result of breathing frequency for the specific patient showing their name.
     * @return - BreathingFrequency enum result showing if the result is Suspicious, Slow, Fast or Normal.
     */
    public BreathingFrequency classifyBreathingFrequency(Patient patient, int respirationRate, boolean print) {
        BreathingFrequency cls;

        if (patient.w <= MIN_WEIGHT || patient.w > MAX_WEIGHT) {
            LOGS.add("Bad weight: " + patient.w);
            throw new IllegalArgumentException("Weight is not in range.");
        }

        if (respirationRate < MIN_SLOW_BREATHING_RATE) {
            cls = BreathingFrequency.SUSPICIOUS;
        } else if (respirationRate < MIN_NORMAL_BREATHING_RATE) {
            cls = BreathingFrequency.SLOW;
        } else if (respirationRate <= MAX_NORMAL_BREATHING_RATE) {
            cls = BreathingFrequency.NORMAL;
        } else {
            cls = BreathingFrequency.FAST;
        }

        if (print) {
            System.out.println("Class result=" + cls + " for " + patient.patient_name);
        }

        return cls;
    }

}


/**
 *  Class of a patient with some basic information.
 */
class Patient {
    public String patient_name;
    public double w;
    public String cond;

    /**
     * Constructs a new patient.
     *
     * @param patient_name - Name of the patient.
     * @param w - How much the patient weights.
     * @param cond - The medical condition of the patient.
     */
    public Patient(String name, double weight, String condition) {
        this.patient_name = name;
        this.w = weight;
        this.cond = condition;
    }
}
