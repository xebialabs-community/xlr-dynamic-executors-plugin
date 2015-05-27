/**
 * THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
 * FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
 */
package com.xebialabs.xlrelease.executors;

import org.apache.commons.collections.list.FixedSizeList;

import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;

/**
 * Created by jdewinne on 5/27/15.
 */
public class ExecutorsHolder {

    public static final ConcurrentMap<String, FixedSizeList> RUNNING_EXECUTORS = new ConcurrentHashMap<String, FixedSizeList>();

    public static synchronized void updateFixedList(String serverName, int index, String taskId) {
        RUNNING_EXECUTORS.get(serverName).set(index, taskId);
    }

    public static synchronized boolean findAndLockExecutor(String serverName, String taskId) {
        FixedSizeList fixedList = RUNNING_EXECUTORS.get(serverName);
        int index = 0;
        for (Object fixedListTaskId : fixedList) {
            if (fixedListTaskId.equals("available")) {
                updateFixedList(serverName, index, taskId);
                return true;
            }
            index++;
        }
        return false;
    }

}
