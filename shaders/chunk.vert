#version 330 core
layout (location = 0) in int in_vertinfo;
layout (location = 1) in int in_color;

const vec3 normal_list[6] = vec3[6](
    vec3(0.0, 0.0, 1.0),
    vec3(0.0, 0.0, -1.0),
    vec3(-1.0, 0.0, 0.0),
    vec3(1.0, 0.0, 0.0),
    vec3(0.0, 1.0, 0.0),
    vec3(0.0, -1.0, 0.0)
    );

const float light_level[6] = float[6](
    0.8,
    0.1,
    0.5,
    0.5,
    1.0,
    0.2
    );
out float light_val;
out vec3 block_color;
uniform vec3 light_dir;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

void main() {
    int x = in_vertinfo >> 27 & 31;
    int y = in_vertinfo >> 22 & 31;
    int z = in_vertinfo >> 17 & 31;
    vec3 in_position = vec3(x,y,z);
    int norm_id = in_vertinfo >> 14 & 7;
    //light_val = light_level[norm_id];
    float r = float(in_color >> 16 & 255) / 255.0;
    float g = float(in_color >> 8 & 255) / 255.0;
    float b = float(in_color & 255) / 255.0;
    block_color = vec3(r,g,b);    
    light_val = max(dot(normal_list[norm_id],normalize(light_dir)),0.1);

    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
}