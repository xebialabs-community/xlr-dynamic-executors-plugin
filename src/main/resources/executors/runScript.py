#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#
import time
from com.xebialabs.deployit.plugin.api.reflect import Type
from com.xebialabs.deployit.repository import SearchParameters

import com.xebialabs.xlrelease.executors.ExecutorsHolder as executors_holder

from java.lang import String
from java.util import Arrays
from org.apache.commons.collections.list import FixedSizeList;

from overtherepy import SshConnectionOptions, OverthereHost, OverthereHostSession

def initialize_executors_holder(servers):
    server_names= []
    for server in servers:
        server_name = server.getProperty("serverName")
        server_names.append(server_name)
        if executors_holder.RUNNING_EXECUTORS.containsKey(server_name):
            print "DEBUG: server name already in RUNNING EXECUTORS [%s]" % server_name
            current_size = executors_holder.RUNNING_EXECUTORS.get(server_name).maxSize()
            if current_size != server.getProperty("nrExecutors"):
                fixed = FixedSizeList.decorate(Arrays.asList(String[server.getProperty("nrExecutors")]));
                executors_holder.RUNNING_EXECUTORS.replace(server_name, fixed)
        else:
            print "DEBUG: server name not in RUNNING EXECUTORS [%s]" % server_name
            fixed = FixedSizeList.decorate(Arrays.asList(["available"] * server.getProperty("nrExecutors")));
            executors_holder.RUNNING_EXECUTORS.put(server_name, fixed)

    # Remove any RUNNING_EXECUTORS that are not in servers
    for key in executors_holder.RUNNING_EXECUTORS.keySet():
        if key not in server_names:
            print "DEBUG: Removing obsolete executors server [%s]" % key
            executors_holder.RUNNING_EXECUTORS.remove(key)

def get_all_executors_servers():
    parameters = SearchParameters().setType(Type.valueOf("executors.Server"))
    executors_servers = _repositoryService.listEntities(parameters)
    return executors_servers

def get_available_executor():
    servers = get_all_executors_servers()
    match = False
    while not match:
        for server in servers:
            if server.getProperty("label") == executorLabel:
                match = True
                print "DEBUG: Trying for executor on server: [%s]" % server.getProperty("serverName")
                if executors_holder.findAndLockExecutor(server.getProperty("serverName"), getCurrentTask().id):
                    print "DEBUG: We did get an executor"
                    return server
                time.sleep(5)
        if match:
            match = False


def execute_script(server):
    print "Running script [%s] on server instance [%s]" % (scriptToExecute, server.getProperty("serverName"))
    sshOpts = SshConnectionOptions(server.getProperty("address"), server.getProperty("username"), password=server.getProperty("password"))
    host = OverthereHost(sshOpts)
    session = OverthereHostSession(host)
    response = session.execute([scriptToExecute], check_success=False)
    if response.rc != 0:
        print "Failed to execute command"
        print response.stderr
    else:
        print "Response", str(response.stdout)

    session.close_conn()

def free_used_executor(server):
    fixedList = executors_holder.RUNNING_EXECUTORS.get(server.getProperty("serverName"))
    for index, taskId in enumerate(fixedList):
        if taskId == getCurrentTask().id:
            print "DEBUG: Freeing up executor with task ID: [%s]" % taskId
            executors_holder.updateFixedList(server.getProperty("serverName"), index, "available")
            return
    print "DEBUG: Task ID [%s] not found for server [%s]" % (getCurrentTask().id, server.getProperty("serverName"))


servers = get_all_executors_servers()
initialize_executors_holder(servers)

server = None
try:
    server = get_available_executor()
    execute_script(server)
finally:
    free_used_executor(server)