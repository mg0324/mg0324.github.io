---
title: springboot多数据源mybatis版
date: 2017-11-06 15:12:34
categories: springboot
tags:
- springboot
- mybatis
---

## springboot多数据源
> 在项目中，一个程序可能需要连接多个数据源，来操作数据，所以需要多数据源的支持。

## 加入mybatis的springboot依赖

	
	<!-- mybatis启动 -->
	<dependency>
		<groupId>org.mybatis.spring.boot</groupId>
		<artifactId>mybatis-spring-boot-starter</artifactId>
		<version>1.3.1</version>
	</dependency>
	<!-- mybatis pagehelper启动 -->
	<dependency>
		<groupId>com.github.pagehelper</groupId>
		<artifactId>pagehelper-spring-boot-starter</artifactId>
		<version>1.2.1</version>
	</dependency>

## springboot集成mybatis多数据源
### 先建立数据源配置文件`DataSourceConfig.java`,其中一个数据源是`@Primary`为默认使用数据源。

	
	package com.inspur.proxy;

	import org.springframework.beans.factory.annotation.Qualifier;
	import org.springframework.beans.factory.annotation.Value;
	import org.springframework.boot.autoconfigure.jdbc.DataSourceBuilder;
	import org.springframework.boot.context.properties.ConfigurationProperties;
	import org.springframework.context.annotation.*;
	import org.springframework.jdbc.datasource.DataSourceTransactionManager;
	import org.springframework.transaction.PlatformTransactionManager;
	import org.springframework.transaction.annotation.EnableTransactionManagement;
	import org.springframework.transaction.annotation.TransactionManagementConfigurer;
	import org.springframework.transaction.jta.JtaTransactionManager;

	import javax.sql.DataSource;


	/**
	 * Created by meigang on 17/10/13.
	 */
	@Configuration
	@ComponentScan
	@EnableTransactionManagement
	public class DataSourceConfig{

	    @Bean(name = "ddwgDS")
	    @ConfigurationProperties(prefix = "spring.datasource.ddwg") // application.properteis中对应属性的前缀
	    @Primary
	    public DataSource dataSource1() {
	        return DataSourceBuilder.create().build();
	    }


	    @Bean(name = "gcsjDS")
	    @ConfigurationProperties(prefix = "spring.datasource.gcsj") // application.properteis中对应属性的前缀
	    public DataSource dataSource2() {
	        return DataSourceBuilder.create().build();
	    }

	    @Bean(name = "ddwgTransactionManager")
	    @Primary
	    public PlatformTransactionManager ddwgTransactionManager(@Qualifier("ddwgDS") DataSource dataSource) {
	        return new DataSourceTransactionManager(dataSource);
	    }

	    @Bean(name = "gcsjTransactionManager")
	    public PlatformTransactionManager gcsjTransactionManager(@Qualifier("gcsjDS") DataSource dataSource) {
	        return new DataSourceTransactionManager(dataSource);
	    }

	}

### `ddwgDS`和`gcsjDS`这2个数据源，启用不同的配置文件前缀，和加载不同的mybatis xml文件路径。
#### `MybatisDbDdwgConfig.java`

	package com.inspur.proxy;

	import org.apache.ibatis.session.SqlSessionFactory;
	import org.mybatis.spring.SqlSessionFactoryBean;
	import org.mybatis.spring.SqlSessionTemplate;
	import org.mybatis.spring.annotation.MapperScan;
	import org.springframework.beans.factory.annotation.Autowired;
	import org.springframework.beans.factory.annotation.Qualifier;
	import org.springframework.context.annotation.Bean;
	import org.springframework.context.annotation.Configuration;
	import org.springframework.context.annotation.Primary;
	import org.springframework.core.io.support.PathMatchingResourcePatternResolver;
	import org.springframework.jdbc.datasource.DataSourceTransactionManager;
	import org.springframework.transaction.annotation.EnableTransactionManagement;

	import javax.sql.DataSource;

	@Configuration
	@MapperScan(basePackages = {"com.inspur.proxy.mapper"}, sqlSessionFactoryRef = "sqlSessionFactoryDdwg")
	public class MybatisDbDdwgConfig {

	    @Autowired
	    @Qualifier("ddwgDS")
	    private DataSource ds;


	    @Bean(name = "sqlSessionFactoryDdwg")
	    @Primary
	    public SqlSessionFactory sqlSessionFactory1() throws Exception {
	        SqlSessionFactoryBean factoryBean = new SqlSessionFactoryBean();
	        factoryBean.setDataSource(ds); // 使用ddwg数据源, 连接ddwg库
	        factoryBean.setMapperLocations(new PathMatchingResourcePatternResolver().getResources("classpath:mybatis/mapper/ddwg/*.xml"));
	        return factoryBean.getObject();

	    }

	    @Bean(name = "sqlSessionTemplateDdwg")
	    @Primary
	    public SqlSessionTemplate sqlSessionTemplate1() throws Exception {
	        SqlSessionTemplate template = new SqlSessionTemplate(sqlSessionFactory1()); // 使用上面配置的Factory
	        return template;
	    }
	}

#### `MybatisDbGcsjConfig.java`


	package com.inspur.proxy;

	import org.apache.ibatis.session.SqlSessionFactory;
	import org.mybatis.spring.SqlSessionFactoryBean;
	import org.mybatis.spring.SqlSessionTemplate;
	import org.mybatis.spring.annotation.MapperScan;
	import org.springframework.beans.factory.annotation.Autowired;
	import org.springframework.beans.factory.annotation.Qualifier;
	import org.springframework.context.annotation.Bean;
	import org.springframework.context.annotation.Configuration;
	import org.springframework.core.io.support.PathMatchingResourcePatternResolver;
	import org.springframework.jdbc.datasource.DataSourceTransactionManager;
	import org.springframework.transaction.annotation.EnableTransactionManagement;

	import javax.sql.DataSource;

	@Configuration
	@MapperScan(basePackages = {"com.inspur.pdata.mapper"}, sqlSessionFactoryRef = "sqlSessionFactoryGcsj")
	public class MybatisDbGcsjConfig {

	    @Autowired
	    @Qualifier("gcsjDS")
	    private DataSource ds;


	    @Bean(name = "sqlSessionFactoryGcsj")
	    public SqlSessionFactory sqlSessionFactory1() throws Exception {
	        SqlSessionFactoryBean factoryBean = new SqlSessionFactoryBean();
	        factoryBean.setDataSource(ds); // 使用gcsj
	        factoryBean.setMapperLocations(new PathMatchingResourcePatternResolver().getResources("classpath:mybatis/mapper/gcsj/*.xml"));
	        return factoryBean.getObject();

	    }

	    @Bean(name = "sqlSessionTemplateGcsj")
	    public SqlSessionTemplate sqlSessionTemplate1() throws Exception {
	        SqlSessionTemplate template = new SqlSessionTemplate(sqlSessionFactory1()); // 使用上面配置的Factory
	        return template;
	    }
	}

### springboot配置文件


	
	#ddwg数据源
	spring.datasource.ddwg.url=jdbc:oracle:thin:@x.x.x.x:1521:orcl
	spring.datasource.ddwg.username=U_QZQD
	spring.datasource.ddwg.password=U_QZQD
	spring.datasource.ddwg.driver-class-name=oracle.jdbc.driver.OracleDriver
	#ddwg连接池配置
	spring.datasource.ddwg.initial-size=20
	spring.datasource.ddwg.min-idle=20
	spring.datasource.ddwg.max-idle=100
	spring.datasource.ddwg.max-wait=30000
	spring.datasource.ddwg.validation-query=SELECT 1 from dual
	#没次使用连接时进行校验，会影响系统性能。默认为false
	spring.datasource.ddwg.test-on-borrow=true
	spring.datasource.ddwg.test-while-idle=true
	spring.datasource.ddwg.test-on-return=true
	spring.datasource.ddwg.remove-abandoned-on-borrow=true
	spring.datasource.ddwg.remove-abandoned-timeout=5
	spring.datasource.ddwg.log-abandoned=true
	#连接池空闲连接的有效时间，设置30分钟
	spring.datasource.ddwg.min-evictable-idle-time-millis=1800000
	#空闲连接回收的时间间隔，与test-while-idle一起使用，设置5分钟
	spring.datasource.ddwg.time-between-eviction-runs-millis=300000

	#过程数据库
	spring.datasource.gcsj.url=jdbc:oracle:thin:@x.x.x.x:1521:DZZWGA
	spring.datasource.gcsj.username=PROCESS_DATA
	spring.datasource.gcsj.password=PROCESS_DATA
	spring.datasource.gcsj.driver-class-name=oracle.jdbc.driver.OracleDriver
	#gcsj连接池配置
	spring.datasource.gcsj.initial-size=20
	spring.datasource.gcsj.min-idle=20
	spring.datasource.gcsj.max-idle=100
	spring.datasource.gcsj.max-wait=30000
	spring.datasource.gcsj.validation-query=SELECT 1 from dual
	#没次使用连接时进行校验，会影响系统性能。默认为false
	spring.datasource.gcsj.test-on-borrow=true
	spring.datasource.gcsj.test-while-idle=true
	spring.datasource.gcsj.test-on-return=true
	spring.datasource.gcsj.remove-abandoned-on-borrow=true
	spring.datasource.gcsj.remove-abandoned-timeout=5
	spring.datasource.gcsj.log-abandoned=true
	#连接池空闲连接的有效时间，设置30分钟
	spring.datasource.gcsj.min-evictable-idle-time-millis=1800000
	#空闲连接回收的时间间隔，与test-while-idle一起使用，设置5分钟
	spring.datasource.gcsj.time-between-eviction-runs-millis=300000