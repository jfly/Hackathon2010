/*
 * Copyright 1999-2004 Carnegie Mellon University.
 * Portions Copyright 2004 Sun Microsystems, Inc.
 * Portions Copyright 2004 Mitsubishi Electric Research Laboratories.
 * All Rights Reserved.  Use is subject to license terms.
 *
 * See the file "license.terms" for information on usage and
 * redistribution of this file, and for a DISCLAIMER OF ALL
 * WARRANTIES.
 *
 */

package hellocube;
import edu.cmu.sphinx.frontend.util.Microphone;
import edu.cmu.sphinx.recognizer.Recognizer;
import edu.cmu.sphinx.result.Result;
import edu.cmu.sphinx.util.props.ConfigurationManager;
import java.lang.String;
import java.util.Properties;
import java.lang.Exception;
import java.io.FileInputStream;

/**
 * HelloCube, bitches.
 */
public class HelloCube {
	public static final String PROPERTIES_FILE = "cubenotation.properties";
	public static Properties properties = new Properties();

    public static void main(String[] args) {
        ConfigurationManager cm;

        if (args.length > 0) {
            cm = new ConfigurationManager(args[0]);
        } else {
            cm = new ConfigurationManager(HelloCube.class.getResource("hellocube.config.xml"));
        }

		// open the properties file
		try {
    		properties.load( HelloCube.class.getResourceAsStream(PROPERTIES_FILE) );
		} catch ( Exception e ) {
			e.printStackTrace();
		}

        // allocate the recognizer
        System.err.println("Loading...");
        Recognizer recognizer = (Recognizer) cm.lookup("recognizer");
        recognizer.allocate();

        // start the microphone or exit if the programm if this is not possible
        Microphone microphone = (Microphone) cm.lookup("microphone");
        if (!microphone.startRecording()) {
            System.err.println("Cannot start microphone.");
            recognizer.deallocate();
            System.exit(1);
        }

        System.err.println("Start speaking. Press Ctrl-C to quit.\n");
        // loop the recognition until the programm exits.
        while (true) {

            Result result = recognizer.recognize();

            if (result != null) {
                String resultText = HelloCube.parseText( result.getBestResultNoFiller() );
                System.out.println( resultText );
				System.err.println( resultText );
            } else {
            }
        }
    }

	private static String parseText( String text ) {
		String[] words = text.split("\\s");
		String commandstr = "";
		for (int i=0; i<words.length; i++ ) {
			commandstr = commandstr + HelloCube.properties.getProperty( words[i] ) + " ";
		}
		if (words == null) {
			commandstr = "";
		}
		return commandstr;
	}

}
