#version 330 core

layout (location = 0) out vec4 fragColor;

in vec3 normal;
in vec3 fragPos;
struct Light {
    vec3 position;
    vec3 Ia;
    vec3 Id;
    vec3 Is;
};
uniform Light light;
uniform vec3 camPos;
vec3 getLight(vec3 color) {
    vec3 Normal = normalize(normal);
    // Ambient
    vec3 ambient = light.Ia;
    // Diffuse
    vec3 lightDir = normalize(light.position - fragPos);
    float diff = max(0, dot(lightDir, Normal));
    vec3 diffuse = diff * light.Id;
    // Specular
    vec3 viewDir = normalize(camPos - fragPos);
    vec3 reflectDir = reflect(-lightDir, Normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0), 32);
    vec3 specular = spec * light.Is;

    return color * (ambient + diffuse + specular);
}

void main() {
    float gamma = 2.2;
    vec3 color = vec3(0.5, 0.0, 0.5);
    // Remove gamma from texture
    //color = pow(color, vec3(gamma));
    color = getLight(color);
    // Fix overall gamma
    color = pow(color, 1 / vec3(gamma));
    fragColor = vec4(color, 1.0);
}