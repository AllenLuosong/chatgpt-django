INSERT INTO chatgpt_config
(id, "key", value, update_datetime, create_datetime, describtion, config_Code)
VALUES(1, 'OPENAI_API_KEY', '', now(), now(),, 'openaiKey配置', 'openai_chat_api_3_5');
INSERT INTO chatgpt_config
(id, "key", value, update_datetime, create_datetime, describtion, config_Code)
VALUES(2, 'OPENAI_API_BASE_URL', '', now(), now(), '调用接口地址，第三方服务', 'openai_chat_api_3_5');
INSERT INTO chatgpt_config
(id, "key", value, update_datetime, create_datetime, describtion, config_Code)
VALUES(3, 'EMAIL_HOST', '', now(), now(), '邮箱服务器配置，用与发送注册邮件', 'email_config');
INSERT INTO chatgpt_config
(id, "key", value, update_datetime, create_datetime, describtion, config_Code)
VALUES(4, 'EMAIL_HOST_USER', '', now(), now(), '邮箱服务器配置，用于发送注册邮件', 'email_config');
INSERT INTO chatgpt_config
(id, "key", value, update_datetime, create_datetime, describtion, config_Code)
VALUES(5, 'DEFAULT_FROM_EMAIL', '', now(), now(), '邮箱服务器配置，用于注册邮件发件人配置', 'email_config');
INSERT INTO chatgpt_config
(id, "key", value, update_datetime, create_datetime, describtion, config_Code)
VALUES(6, 'EMAIL_HOST_PASSWORD', '', now(), now(), '邮箱服务器配置，邮箱服务器登录密码', 'email_config');
INSERT INTO chatgpt_config
(id, "key", value, update_datetime, create_datetime, describtion, config_Code)
VALUES(7, 'EMAIL_PORT', '25', now(), now(), '邮箱服务器端口配置， Linux服务器用587 windows用25', 'email_config');
INSERT INTO chatgpt_config
(id, "key", value, update_datetime, create_datetime, describtion, config_Code)
VALUES(8, 'model', 'gpt-3.5-turbo', now(), now(), '3.5对话模型模型', 'openai_chat_api_3_5');
INSERT INTO chatgpt_config
(id, "key", value, update_datetime, create_datetime, describtion, config_Code)
VALUES(9, 'model', 'gpt-4', now(), now(), '4.0对话模型模型', 'openai_chat_api_4');
INSERT INTO chatgpt_config
(id, "key", value, update_datetime, create_datetime, describtion, config_Code)
VALUES(10, 'model', 'gpt-4-turbo-preview', now(), now(), '4.0对话模型模型', 'openai_chat_api_4');
INSERT INTO chatgpt_config
(id, "key", value, update_datetime, create_datetime, describtion, config_Code)
VALUES(11, 'OPENAI_API_BASE_URL', '', now(), now(), '4.0调用接口地址', 'openai_chat_api_4');
INSERT INTO chatgpt_config
(id, "key", value, update_datetime, create_datetime, describtion, config_Code)
VALUES(12, 'OPENAI_API_KEY', '', now(), now(), '4.0调用openaikey', 'openai_chat_api_4');
INSERT INTO chatgpt_config
(id, "key", value, update_datetime, create_datetime, describtion, config_Code)
VALUES(13, 'OPENAI_API_KEY', '', now(), now(), 'DALL·E 2调用openaikey', 'openai_image_api_DALL_E_2');
INSERT INTO chatgpt_config
(id, "key", value, update_datetime, create_datetime, describtion, config_Code)
VALUES(14, 'OPENAI_API_BASE_URL', '', now(), now(), 'DALL·E 2调用接口地址', 'openai_image_api_DALL_E_2');
INSERT INTO chatgpt_config
(id, "key", value, update_datetime, create_datetime, describtion, config_Code)
VALUES(15, 'model', 'dall-e-2', now(), now(), 'DALL·E 2模型', 'openai_image_api_DALL_E_2');
INSERT INTO chatgpt_config
(id, "key", value, update_datetime, create_datetime, describtion, config_Code)
VALUES(16, 'EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend', now(), now(), '使用django自带邮箱后台', 'email_config');
INSERT INTO chatgpt_config
(id, "key", value, update_datetime, create_datetime, describtion, config_Code)
VALUES(17, 'VERIFICATION_REDIRECT_URL', '', now(), now(), '注册链接', 'email_config');
INSERT INTO chatgpt_config
(id, "key", value, update_datetime, create_datetime, describtion, config_Code)
VALUES(18, 'EMAIL_SUBJECT', 'AI-Chat网站验证', now(), now(), '发送的注册邮件主题', 'email_config');
