#version 330 core
layout (location = 0) in int in_vertinfo;
const vec3 normal_list[6] = vec3[6](
    vec3(0, 0, 1),
    vec3(0, 0, -1),
    vec3(-1, 0, 0),
    vec3(1, 0, 0),
    vec3(0, 1, 0),
    vec3(0, -1, 0)
    );
out vec3 normal;
out vec3 fragPos;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

void main() {
    int x = in_vertinfo >> 27 & 31;
    int y = in_vertinfo >> 22 & 31;
    int z = in_vertinfo >> 17 & 31;
    vec3 in_position = vec3(x,y,z);
    int norm_id = in_vertinfo >> 14 & 7;
    // Get fragment in worldspace
    vec3 temp_norm = normal_list[norm_id];
    fragPos = vec3(m_model * vec4(in_position, 1.0));
    normal = mat3(transpose(inverse(m_model))) * normalize(temp_norm);
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
}