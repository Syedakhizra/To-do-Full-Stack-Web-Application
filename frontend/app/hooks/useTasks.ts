import { useState, useEffect } from 'react';
import apiClient from '../lib/api-client';
import { Task, TaskCreateRequest, TaskUpdateRequest, TaskCreateApiRequest } from '../lib/types';
import { useAuth } from '../context/auth-context';

export const useTasks = () => {
  const { user } = useAuth(); // Get the authenticated user
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch all tasks for the authenticated user
  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await apiClient.get<Task[]>('/api/v1/users/me/tasks');
      setTasks(response.data);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch tasks');
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  // Create a new task
  const createTask = async (taskData: TaskCreateRequest) => {
    try {
      setLoading(true);
      setError(null);

      // Convert to API request format by adding user_id from auth context
      const apiRequest: TaskCreateApiRequest = {
        ...taskData,
        user_id: user?.id || 0 // Use authenticated user ID, fallback to 0 if not available
      };

      const response = await apiClient.post<Task>('/api/v1/tasks', apiRequest);
      setTasks([...tasks, response.data]);
      return response.data;
    } catch (err: any) {
      setError(err.message || 'Failed to create task');
      console.error('Error creating task:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Update an existing task
  const updateTask = async (taskId: string, taskData: TaskUpdateRequest) => {
    try {
      setLoading(true);
      setError(null);

      // Pass taskData directly since it doesn't include user_id
      const response = await apiClient.put<Task>(`/api/v1/users/me/tasks/${taskId}`, taskData);

      // Update the task in the local state
      setTasks(tasks.map(task =>
        task.id === taskId ? response.data : task
      ));

      return response.data;
    } catch (err: any) {
      setError(err.message || 'Failed to update task');
      console.error('Error updating task:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Toggle task completion status
  const toggleTaskCompletion = async (taskId: string) => {
    try {
      const task = tasks.find(t => t.id === taskId);
      if (!task) {
        throw new Error('Task not found');
      }

      setLoading(true);
      setError(null);

      // Use PUT to update the task with toggled completion status
      const response = await apiClient.put<Task>(
        `/api/v1/users/me/tasks/${taskId}`,
        {
          title: task.title,
          description: task.description || null,
          completed: !task.completed
        }
      );

      // Update the task in the local state
      setTasks(tasks.map(t =>
        t.id === taskId ? response.data : t
      ));

      return response.data;
    } catch (err: any) {
      setError(err.message || 'Failed to update task status');
      console.error('Error toggling task completion:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Delete a task
  const deleteTask = async (taskId: string) => {
    try {
      setLoading(true);
      setError(null);

      await apiClient.delete(`/api/v1/users/me/tasks/${taskId}`);

      // Remove the task from the local state
      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (err: any) {
      setError(err.message || 'Failed to delete task');
      console.error('Error deleting task:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Initialize tasks when the hook is first used
  useEffect(() => {
    fetchTasks();
  }, []);

  return {
    tasks,
    loading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    toggleTaskCompletion,
    deleteTask,
  };
};