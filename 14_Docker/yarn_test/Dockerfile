FROM centos:7
MAINTAINER Maksim wardomenmax@gmail.com
LABEL HDFS Hadoop

RUN yum clean all && \
	yum list updates && \  
	yum -y install java-1.8.0-openjdk-devel
RUN yum -y install wget
RUN yum -y install openssh-server openssh-clients

ENV JAVA_HOME /usr/lib/jvm/java-1.8.0-openjdk
ENV PATH $PATH:$JAVA_HOME/bin
ENV HADOOP_HOME /usr/local/hadoop
ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop

ARG HOST_NAME=scylla
ARG CLIENT_NAME=charybdis
ARG HADOOP_VERSION=3.1.2

RUN wget https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz && \
	tar -xzvf hadoop-${HADOOP_VERSION}.tar.gz -C /usr/local && \
	mv /usr/local/hadoop-${HADOOP_VERSION} /usr/local/hadoop

RUN groupadd hadoop && useradd -g hadoop hadoop && useradd -g hadoop yarn && useradd -g hadoop hdfs

RUN mkdir -p /opt/mount{1..2}/datanode-dir && \
	chown hdfs:hadoop /opt/mount{1..2}/datanode-dir && \
	mkdir /opt/mount{1..2}/nodemanager-local-dir && \
	mkdir /opt/mount{1..2}/nodemanager-log-dir && \
	chown hdfs:hadoop /opt/mount{1..2}/nodemanager-local-dir && \
	chown hdfs:hadoop /opt/mount{1..2}/nodemanager-log-dir
 


VOLUME [ "/opt/mount1/datanode-dir ", "/opt/mount2/datanode-dir ", "/hadoop/dfs/sname1", "/hadoop/dfs/data1" ]

RUN mkdir -p /home/hadoop/.ssh && \
	ssh-keygen -t rsa -P '' -f  /home/hadoop/.ssh/hadoop_key && \
	cat /home/hadoop/.ssh/hadoop_key.pub >> /home/hadoop/.ssh/authorized_keys

RUN wget https://gist.githubusercontent.com/rdaadr/2f42f248f02aeda18105805493bb0e9b/raw/6303e424373b3459bcf3720b253c01373666fe7c/hadoop-env.sh -O /usr/local/hadoop/hadoop-env.sh
RUN wget https://gist.githubusercontent.com/rdaadr/64b9abd1700e15f04147ea48bc72b3c7/raw/2d416bf137cba81b107508153621ee548e2c877d/core-site.xml -O /usr/local/hadoop/core-site.xml
RUN wget https://gist.githubusercontent.com/rdaadr/2bedf24fd2721bad276e416b57d63e38/raw/640ee95adafa31a70869b54767104b826964af48/hdfs-site.xml -O /usr/local/hadoop/hdfs-site.xml 
RUN wget https://gist.githubusercontent.com/Stupnikov-NA/ba87c0072cd51aa85c9ee6334cc99158/raw/bda0f760878d97213196d634be9b53a089e796ea/yarn-site.xml -O /usr/local/hadoop/yarn-site.xml

RUN sed -i '/^export JAVA_HOME/s/=.*$/=\/usr\/lib\/jvm\/java-1\.8\.0-openjdk/' /usr/local/hadoop/hadoop-env.sh && \
	sed -i '/^export HADOOP_HOME/s/=.*$/=\/usr\/local\/hadoop/' /usr/local/hadoop/hadoop-env.sh

RUN sed -Ei 's/([\%])\w+[\%]/$CLIENT_NAME/g' /usr/local/hadoop/core-site.xml

RUN sed -Ei 's/([\%])DATANODE_DIRS[\%]/\/opt\/mount1\/datanode-dir\,\/opt\/mount2\/datanode-dir/g ; s/([\%])NAMENODE_DIRS[\%]/\/opt\/mount1\/namenode-dir\,\/opt\/mount2\/namenode-dir/g' /usr/local/hadoop/hdfs-site.xml

RUN sed -Ei 's/([\%])YARN_RESOURCE_MANAGER_HOSTNAME[\%]/$CLIENT_NAME/g ; \
	s/([\%])NODE_MANAGER_LOCAL_DIR[\%]/\/opt\/mount1\/nodemanager-local-dir\,\/opt\/mount2\/nodemanager-local-dir/g ; \
	s/([\%])NODE_MANAGER_LOG_DIR[\%]/\/opt\/mount1\/nodemanager-log-dir\,\/opt\/mount2\/nodemanager-log-dir/g' /usr/local/hadoop/yarn-site.xml

RUN chmod +x /usr/local/hadoop

ADD start-hdfs.sh start-yarn.sh

USER hdfs

EXPOSE 9000 50010 50020 50070 50075 50090

ENTRYPOINT ["bash", "start-hdfs.sh"]

USER yarn

EXPOSE 8030 8031 8032 8033 8040 8042 8088

CMD ["start-yarn.sh"]

