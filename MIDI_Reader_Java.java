import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.PrintWriter;
import javax.sound.midi.MidiEvent;
import javax.sound.midi.MidiMessage;
import javax.sound.midi.MidiSystem;
import javax.sound.midi.Sequence;
import javax.sound.midi.ShortMessage;
import javax.sound.midi.Track;

public class MIDI_Reader_Java {

    
    public static final int NOTE_ON = 0x90;
    public static final int NOTE_OFF = 0x80;

    public static void main(String[] args) throws Exception {
        File midiFile = new File("javaBridge.txt");
        BufferedReader br = new BufferedReader(new FileReader(midiFile));
        String st = br.readLine();
        Sequence sequence = MidiSystem.getSequence(new File(st));
        br.close();

        PrintWriter writer = new PrintWriter("MIDI_Unpacked.txt", "UTF-8");
        for (Track track :  sequence.getTracks()) {
            int chanelComp = 999;
            for (int i=0; i < track.size(); i++) { 
                MidiEvent event = track.get(i);
                MidiMessage message = event.getMessage();
                if (message instanceof ShortMessage sm) {
                    if (sm.getCommand() == NOTE_ON) {
                        int key = sm.getData1();
                        int velocity = sm.getData2();
                        int chanel = sm.getChannel();
                        if (chanel != chanelComp) {
                            writer.println("channel="+chanel);
                            chanelComp = chanel;
                        }
                        if (velocity >= 1) {
                            writer.println(event.getTick() + ","+ key);
                        }
                    } 
                }
            }
        }
        
        writer.close();
    }
}