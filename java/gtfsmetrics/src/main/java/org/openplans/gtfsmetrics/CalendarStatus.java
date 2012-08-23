package org.openplans.gtfsmetrics;

import java.io.File;
import java.io.IOException;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import org.joda.time.DateTime;
import org.joda.time.Days;
import org.onebusaway.gtfs.impl.GtfsDaoImpl;
import org.onebusaway.gtfs.model.AgencyAndId;
import org.onebusaway.gtfs.model.ServiceCalendar;
import org.onebusaway.gtfs.model.ServiceCalendarDate;
import org.onebusaway.gtfs.model.calendar.ServiceDate;
import org.onebusaway.gtfs.serialization.GtfsReader;


public class CalendarStatus {
    public static void main( String[] args ) {
        GtfsReader reader = new GtfsReader();
        try {
            reader.setInputLocation(new File(args[0]));
        } catch (IOException e1) {
            // TODO Auto-generated catch block
            e1.printStackTrace();
        }
        
        GtfsDaoImpl store = new GtfsDaoImpl();
        reader.setEntityStore(store);

        try {
            reader.run();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        
        
        Map<AgencyAndId, Set<ServiceDate>> addExceptions = new HashMap<AgencyAndId, Set<ServiceDate>>();
        Map<AgencyAndId, Set<String>> removeExceptions = new HashMap<AgencyAndId, Set<String>>();
        for(ServiceCalendarDate date : store.getAllCalendarDates()) {
            if(date.getExceptionType() == ServiceCalendarDate.EXCEPTION_TYPE_ADD) {
                Set<ServiceDate> dateSet = addExceptions.get(date.getServiceId());
                if(dateSet == null) {
                    dateSet = new HashSet<ServiceDate>();
                    addExceptions.put(date.getServiceId(), dateSet);
                }
                dateSet.add(date.getDate());
            }
            else if(date.getExceptionType() == ServiceCalendarDate.EXCEPTION_TYPE_REMOVE) {
                Set<String> dateSet = removeExceptions.get(date.getServiceId());
                if(dateSet == null) {
                    dateSet = new HashSet<String>();
                    removeExceptions.put(date.getServiceId(), dateSet);
                }
                dateSet.add(constructMDYString(date.getDate()));
            }
        }
        
        DateTime latestEnd = new DateTime(0);
        
        for (ServiceCalendar svcCal : store.getAllCalendars()) {
        
            DateTime start = new DateTime(svcCal.getStartDate().getAsDate().getTime());
            DateTime end = new DateTime(svcCal.getEndDate().getAsDate().getTime());
            
            int days = Days.daysBetween(start, end).getDays();
            for(int d=0; d < days; d++) {
                int gd = getDay(svcCal, end.dayOfWeek().get());// dateCal.get(Calendar.DAY_OF_WEEK));
                boolean removeException = false;
                Set<String> dateSet = removeExceptions.get(svcCal.getServiceId());
                if(dateSet != null) {
                	removeException = dateSet.contains(constructMDYString(end));
                }
                if(gd == 1 && !removeException) break;
                end = end.minusDays(1);
            }
            if(end.isAfter(latestEnd)) latestEnd = end;
            
        }
        
        for(Set<ServiceDate> dateSet: addExceptions.values()) {
            for(ServiceDate sd : dateSet) {
                DateTime dt = new DateTime(sd.getAsDate().getTime());
                if(dt.isAfter(latestEnd)) latestEnd = dt;
            }
        }
        
        System.out.print(Days.daysBetween(new DateTime(), latestEnd).getDays());
        
    }
    
    private static int getDay(ServiceCalendar cal, int dow) {
        switch(dow) {
            case 1: return cal.getMonday();
            case 2: return cal.getTuesday();
            case 3: return cal.getWednesday();
            case 4: return cal.getThursday();
            case 5: return cal.getFriday();
            case 6: return cal.getSaturday();
            case 7: return cal.getSunday();
        }
        return 0;
    }
    
    private static String constructMDYString(ServiceDate date) {
        return date.getMonth()+"-"+date.getDay()+"-"+date.getYear();
    }
    
    private static String constructMDYString(DateTime dt) {
        return dt.getMonthOfYear()+"-"+dt.getDayOfMonth()+"-"+dt.getYear();
    }

}
