FROM centos:7
MAINTAINER Maksim wardomenmax@gmail.com
LABEL HDFS Hadoop

RUN yum update && \
        yum install java-1.8.0-openjdk-devel && \
        yum -y install wget

ENV JAVA_HOME /usr/lib/jvm/java-1.8.0-openjdk
ENV PATH $PATH:$JAVA_HOME/bin
ENV HADOOP_HOME /usr/local/hadoop
ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop


RUN mkdir downloads \
        cd downloads

RUN wget https://archive.apache.org/dist/hadoop/common/hadoop-3.1.2/hadoop-3.1.2.tar.gz | tar -xzvf hadoop-3.1.2.tar.gz -C /usr/local && \
         mv /usr/local/hadoop-3.1.2 /usr/local/hadoop

RUN groupadd hadoop && sudo useradd -g hadoop hadoop && sudo useradd -g hadoop yarn && sudo useradd -g hadoop hdfs

RUN mkdir -p /opt/mount{1..2}/namenode-dir && \
        chown hdfs:hadoop /opt/mount{1..2}/namenode-dir



VOLUME [ "/opt/mount1/namenode-dir ", "/opt/mount2/namenode-dir ", "/hadoop/dfs/sname1", "/hadoop/dfs/data1" ]

RUN ssh-keygen -q -N "" -t rsa -f  /home/hadoop/.ssh/hadoop_key && \
        ssh-copy-id -i ~/.ssh/hadoop_key.pub /home/hadoop/.ssh/authorized_keys

RUN wget https://gist.githubusercontent.com/rdaadr/2f42f248f02aeda18105805493bb0e9b/raw/6303e424373b3459bcf3720b253c01373666fe7c/hadoop-env.sh -O /usr/local/hadoop/current/hadoop-3.1.2/etc/hadoop/hadoop-en$
        wget https://gist.githubusercontent.com/rdaadr/64b9abd1700e15f04147ea48bc72b3c7/raw/2d416bf137cba81b107508153621ee548e2c877d/core-site.xml -O /usr/local/hadoop/current/hadoop-3.1.2/etc/hadoop/core-$
        wget https://gist.githubusercontent.com/rdaadr/2bedf24fd2721bad276e416b57d63e38/raw/640ee95adafa31a70869b54767104b826964af48/hdfs-site.xml -O /usr/local/hadoop/current/hadoop-3.1.2/etc/hadoop/hdfs-$
        wget https://gist.githubusercontent.com/Stupnikov-NA/ba87c0072cd51aa85c9ee6334cc99158/raw/bda0f760878d97213196d634be9b53a089e796ea/yarn-site.xml -O /usr/local/hadoop/current/hadoop-3.1.2/etc/hadoop$

RUN sed -i '/^export JAVA_HOME/s/=.*$/=\/usr\/lib\/jvm\/java-1\.8\.0-openjdk/' /usr/local/hadoop/current/hadoop-3.1.2/etc/hadoop/hadoop-env.sh && \
        sed -i '/^export HADOOP_HOME/s/=.*$/=\/usr\/local\/hadoop\/current\/hadoop-3\.1\.2/' /usr/local/hadoop/current/hadoop-3.1.2/etc/hadoop/hadoop-env.sh

RUN hn=HOSTNAME && \
        sed -Ei 's/([\%])\w+[\%]/hn/g' /usr/local/hadoop/current/hadoop-3.1.2/etc/hadoop/core-site.xml

RUN sed -Ei 's/([\%])DATANODE_DIRS[\%]/\/opt\/mount1\/datanode-dir\,\/opt\/mount2\/datanode-dir/g ; && \
        s/([\%])NAMENODE_DIRS[\%]/\/opt\/mount1\/namenode-dir\,\/opt\/mount2\/namenode-dir/g' /usr/local/hadoop/current/hadoop-3.1.2/etc/hadoop/hdfs-site.xml

RUN sed -Ei 's/([\%])YARN_RESOURCE_MANAGER_HOSTNAME[\%]/scylla/g ; && \
        s/([\%])NODE_MANAGER_LOCAL_DIR[\%]/\/opt\/mount1\/nodemanager-local-dir\,\/opt\/mount2\/nodemanager-local-dir/g ; && \
        s/([\%])NODE_MANAGER_LOG_DIR[\%]/\/opt\/mount1\/nodemanager-log-dir\,\/opt\/mount2\/nodemanager-log-dir/g' /usr/local/hadoop/current/hadoop-3.1.2/etc/hadoop/yarn-site.xml

RUN chmod g+s -R /usr/local/hadoop && \
        chmod g+w -R /usr/local/hadoop

USER hdfs

EXPOSE 9000 50010 50020 50070 50075 50090

CMD ["bash", "start-hdfs.sh"]
